from typing import Annotated
from urllib.parse import unquote
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from requests import Session
from sqlalchemy import or_,select
from sqlalchemy.orm import joinedload
from app.auth import get_current_user
import app.models as models
from passlib.context import CryptContext
from .database import engine,SessionLocal

router = APIRouter(
    tags=['users']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

class StudentBase(BaseModel):
    StudentID: int
    FirstName: str
    LastName : str
    Email: str
    password: str
    pin: str
    Year : str
    Degree: str
    FacultyName: str
    Department: str
    
class Auth_pwd(BaseModel):
    Email: str
    password : str
    
class Auth_pin(BaseModel):
    Email: str
    pin: str
    
class Personnel(BaseModel):
    FirstName: str
    LastName : str
    Email: str
    password: str
    pin:str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/user/getAllusers",status_code=status.HTTP_200_OK)
async def getAll_users(db:db_dependency):
    users = db.query(models.Student).options(joinedload(models.Student.auth_users)).all()
    return users

@router.post("/Register/user",status_code=status.HTTP_201_CREATED)
async def create_user(user: StudentBase,db:db_dependency):
    check_email = db.query(models.Auth_users).filter(models.Auth_users.Email == user.Email).first()
    print(check_email)
    if check_email != None:
        raise HTTPException(status_code=404,detail='Bad request')
    else:
        db_user = models.Student(StudentID=user.StudentID,
                                    FirstName=user.FirstName,
                                    LastName=user.LastName,
                                    Email=user.Email,
                                    Year=user.Year,
                                    Degree=user.Degree,
                                    FacultyName=user.FacultyName,
                                    Department=user.Department)
        db.add(db_user)
        db_auth = models.Auth_users(Email=user.Email,password=pwd_context.hash(user.password),Roll="Student",pin=pwd_context.hash(user.pin))
        db.add(db_auth)
        db.commit()
        return status.HTTP_201_CREATED
        

@router.post("/Register/staff",status_code=status.HTTP_201_CREATED)
async def create_user(user: Personnel,db:db_dependency):
    db_user = models.Personnel(FirstName=user.FirstName,
                                LastName=user.LastName,
                                Email=user.Email,
)
    db.add(db_user)
    db_auth = models.Auth_users(Email=user.Email,password=pwd_context.hash(user.password),Roll="Teacher",pin=pwd_context.hash(user.pin))
    db.add(db_auth)
    db.commit()
    return status.HTTP_201_CREATED
    
@router.get("/users/{ID_EMAIL}",status_code=status.HTTP_200_OK)
async def read_user(ID_EMAIL:str | str ,db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)]):
    ID_EMAIL = unquote(ID_EMAIL)
    #user = db.query(models.Student).filter(or_(models.Student.StudentID == ID_EMAIL,models.Student.Email == ID_EMAIL)).all()
    stmt = select(models.Student).where(or_(models.Student.StudentID.like(f"{ID_EMAIL}%"),models.Student.Email.like(f"{ID_EMAIL}%")))
    result = db.execute(stmt)
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404,detail='User not found')
    return users

@router.patch("/users/changepwd",status_code=status.HTTP_202_ACCEPTED)
async def update_password(data:Auth_pwd,db:db_dependency):
    db_user_auth = db.query(models.Auth_users).filter(
        models.Auth_users.Email == data.Email).first()
    if db_user_auth:
        db_user_auth.password = pwd_context.hash(data.password)
        db.commit()
        return {"message":"Password updated successfully"}
    else:
        raise HTTPException(status_code=404,detail="Error")
    
@router.patch("/users/changepin",status_code=status.HTTP_202_ACCEPTED)
async def update_pin(data:Auth_pin,db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)]):
    db_user_auth = db.query(models.Auth_users).filter(
        models.Auth_users.Email == data.Email).first()
    if db_user_auth:
        db_user_auth.pin = pwd_context.hash(data.pin)
        db.commit()
        return {"message":"Password updated successfully"}
    else:
        raise HTTPException(status_code=404,detail="Error")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/verifyPIN",status_code=status.HTTP_200_OK)
async def verify_pin(data:Auth_pin,db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)]):
    db_user_auth = db.query(models.Auth_users).filter(
        models.Auth_users.Email == data.Email).first()
    if not db_user_auth:
        raise HTTPException(status_code=404)
    if not verify_password(data.pin, db_user_auth.pin):
        raise HTTPException(status_code=404)
    return {"message": "PIN verified successfully"}
        
    
    