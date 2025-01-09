from datetime import datetime, timedelta
from io import BytesIO
import re
from typing import Annotated, Union
import cv2
from fastapi import APIRouter, Depends, FastAPI, File, UploadFile, status, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import numpy as np
from pydantic import BaseModel
import app.models as models
from passlib.context import CryptContext
from model.face_recog import predict
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from sqlalchemy.orm import joinedload
SECRET_KEY = "b407ee842d5ff2341fbb84f6dde807661958483323ec5e4c0963ed976daeb328"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class TokenData(BaseModel):
    Email: str
    Roll:str

class PinAuth(BaseModel):
    pin: str

db_dependency = Annotated[Session, Depends(get_db)]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ฟังก์ชันสำหรับการตรวจสอบรหัสผ่าน
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ฟังก์ชันสำหรับการเรียกใช้ข้อมูลผู้ใช้จากฐานข้อมูล
def get_user_by_Email(db, Email: str):
    return db.query(models.Auth_users).filter(models.Auth_users.Email == Email).first()

def get_user_by_ID(db, ID:str):
    return db.query(models.Student).options(joinedload(models.Student.auth_users)).filter(models.Student.StudentID == ID).first()

def login_with_pin(db,Email:str,pin:str):
    user = get_user_by_Email(db, Email)
    if not user:
        return False
    if not verify_password(pin, user.pin):
        return False
    return user

# ฟังก์ชันสำหรับการตรวจสอบข้อมูลผู้ใช้
def authenticate_user(db, Email: str, password: str):
    user = get_user_by_Email(db, Email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def face_authenticate_user(db, ID: str):
    user = get_user_by_ID(db=db,ID=ID)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user
    
# ฟังก์ชันสำหรับสร้าง Token
def create_access_token(data: dict,expires_date: timedelta):
    # สามารถใช้ไลบรารี่อื่น ๆ เพื่อสร้าง Token ได้
    encode = {'Email':data['Email']}
    encode2 = {'Roll':data['Roll']}
    encode.update(encode2)
    expires = datetime.utcnow() + expires_date
    encode.update({'exp': expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db:db_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        Email: str = payload.get('Email')
        Roll: str = payload.get('Roll')
        
        if Email:
            if Roll == 'Student':
                db_query = db.query(models.Student).options(joinedload(models.Student.auth_users).load_only(models.Auth_users.Roll)).filter(models.Student.Email == Email).first()
                # ตรวจสอบว่า db_query ไม่เป็น None ก่อนการ return
                if db_query is not None:
                    return db_query
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found1.')
            else:
                db_query = db.query(models.Personnel).options(joinedload(models.Personnel.auth_users).load_only(models.Auth_users.Roll)).filter(models.Personnel.Email == Email).first()
                # ตรวจสอบว่า db_query ไม่เป็น None ก่อนการ return
                if db_query is not None:
                    return db_query
                else:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found2.')
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Error validating token.')
    
    
# เรียกใช้ API endpoint สำหรับการ login
@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # สร้าง Token จากข้อมูลผู้ใช้
    access_token = create_access_token({'Email': user.Email,'Roll': user.Roll},timedelta(days=30))
    return {"access_token": access_token, "token_type": "bearer"}

# เรียกใช้ API endpoint ด้วย Token ที่สร้างมา
@router.get("/users/me")
async def read_users_me(current_user: Annotated[dict,Depends(get_current_user)]):
    return current_user

@router.post("/login/")
async def login_pin(db:db_dependency, data: PinAuth, current_user: Annotated[dict,Depends(get_current_user)]):
    Email = current_user.Email
    user = login_with_pin(db,Email,data.pin)
    if user is False:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect PIN",
        )
    return {"message": "Login successful"}

@router.post("/face_rocognition_login")
async def recog(db:db_dependency,file: UploadFile = File(...)):
    contents = await file.read()
    img_np = np.frombuffer(contents, np.uint8)
    img_np = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    if img_np is None:
        return JSONResponse(content={"error": "Invalid image format"}, status_code=400)
    prediction = predict(img_np)
    match = re.search(r'\b\d{11}\b', str(prediction))
    number = match.group()
    if prediction is not None:
        user = face_authenticate_user(db=db, ID=number)
        access_token = create_access_token({'Email': user.Email,'Roll': user.auth_users.Roll},timedelta(days=30))
        return {"access_token": access_token, "token_type": "bearer"}
        #return user
    else:
        return JSONResponse(content={"error": "No face detected"}, status_code=400)
    