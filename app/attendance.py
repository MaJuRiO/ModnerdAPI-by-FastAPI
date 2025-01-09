from datetime import datetime, timedelta
import random
import re
import string
from typing import Annotated, Union
import cv2
from fastapi import APIRouter, Depends, FastAPI, File, UploadFile, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import numpy as np
from pydantic import BaseModel
from app.auth import face_authenticate_user, get_current_user
import app.models as models
from passlib.context import CryptContext
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from sqlalchemy.orm import joinedload
from model.face_recog import predict

router = APIRouter(
    tags=['attendance']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class AttendancesBase(BaseModel):
    StudentID:str
    date:str
    course_code:str

class AttendancesBaseV2(BaseModel):
    Course_code:str
    Date:str

class courseCODE(BaseModel):
    Course_code:str
    Date:str
    
class updateTime(BaseModel):
    Course_code:str
    time:str
    
def check_time_in_range(start_time_str, end_time_str):
    # แปลงเวลาเริ่มต้นและเวลาสิ้นสุดเป็น time object
    start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
    end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
    
    # เวลาปัจจุบัน
    current_time = datetime.now().time()
    
    # ตรวจสอบว่าเวลาปัจจุบันอยู่ในช่วงเวลาหรือไม่
    if start_time <= current_time <= end_time:
        # แปลงเวลาปัจจุบันและเวลาเริ่มต้นเป็น datetime object สำหรับคำนวณเวลา
        current_datetime = datetime.combine(datetime.today(), current_time)
        start_datetime = datetime.combine(datetime.today(), start_time)
        
        # คำนวณความต่างของเวลา
        time_difference = current_datetime - start_datetime
        
        # เช็คว่าความต่างของเวลามากกว่า 30 นาทีหรือไม่
        if time_difference > timedelta(minutes=30):
            return "Late"
        else:
            return "Present"
    else:
        return False
    
@router.patch('/update_latetime',status_code=status.HTTP_200_OK)
async def update_time(time:updateTime,db:db_dependency):
    query_course = db.query(models.Course).filter(models.Course.Course_code == time.Course_code).first()
    if query_course:
        if time.time != None:
            query_course.late_time = time.time    
            db.commit()
            db.refresh(query_course)
            return {"message": "Course updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Course not found")
    
@router.patch('/attendance_checkin',status_code=status.HTTP_200_OK)
async def checkin(current_user: Annotated[dict,Depends(get_current_user)],data:AttendancesBaseV2,db:db_dependency):
    #user = face_recog_model
    if current_user:
        db_attendance = db.query(models.Attendance).options(joinedload(models.Attendance.course_detail)).filter(
            models.Attendance.StudentID == current_user.StudentID,
            models.Attendance.Course_code == data.Course_code,
            models.Attendance.Date == data.Date
        ).first()
        
        current_time = datetime.now().time()
        
        if db_attendance:
            if db_attendance.Status == 'NotYet':
                course_detail = db_attendance.course_detail
                start_time = course_detail.start_time
                end_time = course_detail.end_time
                
                if start_time <= current_time <= end_time:
                    time_difference = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), start_time)
                    
                    late_time = db.query(models.Course.late_time).filter(models.Course.Course_code==data.Course_code).first()
                    if time_difference <= timedelta(minutes=float(late_time)):
                        db_attendance.Status = 'Present'
                    else:
                        db_attendance.Status = 'Late'
                    
                    db.commit()
                    db.refresh(db_attendance)
                    return {"message": "Attendance updated successfully"}
                else:
                    raise HTTPException(status_code=404, detail="It's not yet time for the class to start.")
            else:
                raise HTTPException(status_code=404, detail="Already Check in")
        else:
            raise HTTPException(status_code=404, detail="Attendance not found")


@router.post('/attendance',status_code=status.HTTP_200_OK)
async def get_attendance(data:AttendancesBase,db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)]):
    attendances = db.query(models.Attendance).options(joinedload(models.Attendance.course_detail)).filter(models.Attendance.StudentID == data.StudentID,
                                                                                                            models.Attendance.Course_code == data.course_code,
                                                                                                            models.Attendance.Date==data.date).first()
    return attendances

@router.patch('/update_attendance',status_code=status.HTTP_200_OK)
async def update_attendance(data:AttendancesBase,db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)]):
    db_attendance = db.query(models.Attendance).filter(
        models.Attendance.StudentID == data.StudentID,
        models.Attendance.Course_code == data.Course_code,
        models.Attendance.Date == data.Date
    ).first()
    if db_attendance:
        db_attendance.Status = data.Status
        db.commit()
        db.refresh(db_attendance)
        return {"message": "Attendance updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Attendance not found")

def generate_code():
    # สุ่มตัวอักษรและตัวเลขขึ้นมา 6 ตัว
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(6))
    return code

@router.patch('/update_course_code',status_code=status.HTTP_201_CREATED)
async def update_course_code(data:courseCODE,db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)]):
    db_course_check = db.query(models.course_check).filter(models.course_check.Course_code == data.Course_code).first()
    
    if db_course_check is None:
        code = generate_code()
        db_create_course_check = models.course_check(Course_code=data.Course_code,code=code,Date=data.Date)
        db.add(db_create_course_check)
        db.commit()
        return status.HTTP_201_CREATED,{"message": "Course code create successfully"},{"Course_code":code}
    else:
        code = generate_code()
        db_course_check.code = code
        db_course_check.Date = data.Date
        db.commit()
        db.refresh(db_course_check)
        return {"message": "Course code updated successfully","Course_code":code}
    
@router.post('/Get_course_code',status_code=status.HTTP_200_OK)
async def get_course_code(data:courseCODE,db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)]):
    db_course_check = db.query(models.course_check).filter(models.course_check.Course_code == data.Course_code).first()
    if db_course_check is None:
        code = generate_code()
        db_create_course_check = models.course_check(Course_code=data.Course_code,code=code,Date=data.Date)
        db.add(db_create_course_check)
        db.commit()
        return code
    else:
        return db_course_check.code
    
    
class classname(BaseModel):
    studentId:str
    coursecode:str
    code:str
        

@router.post('/checkclassname',status_code=status.HTTP_200_OK)
async def check_class_name(data:classname,db:db_dependency):
    db_st = db.query(models.Enrollment).filter(models.Enrollment.StudentID==data.studentId,models.Enrollment.Course_code==data.coursecode).first()
    if db_st != None:
        db_check = db.query(models.course_check).filter(models.course_check.Course_code == data.coursecode,models.course_check.code == data.code).first()
        if db_check != None:
            return status.HTTP_200_OK
        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE)
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
@router.post('/Face_checkin',status_code=status.HTTP_200_OK)
async def recog(db:db_dependency,current_user: Annotated[dict,Depends(get_current_user)],file: UploadFile = File(...)):
    contents = await file.read()
    img_np = np.frombuffer(contents, np.uint8)
    img_np = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    if img_np is None:
        raise JSONResponse(content={"error": "Invalid image format"}, status_code=400)
    prediction = predict(img_np)
    match = re.search(r'\b\d{11}\b', str(prediction))
    number = match.group()
    if prediction is not None:
        if number == current_user.StudentID:
            return {"message": "Checkin successful"}
        else:
            raise JSONResponse(content={"error": "Face not match"}, status_code=400)
    else:
        raise JSONResponse(content={"error": "No face detected"}, status_code=400)