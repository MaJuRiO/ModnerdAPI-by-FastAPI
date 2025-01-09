from datetime import datetime , timedelta
from typing import Annotated, Union
from fastapi import Depends, FastAPI, File, UploadFile, status, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from pydantic import BaseModel
from .database import engine,SessionLocal
from sqlalchemy import or_ 
from sqlalchemy.orm import Session,joinedload
import app.auth as auth,app.users as users,app.GCS as GCS,app.attendance as attendance,app.professor as professor
import app.models as models
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(GCS.router)
app.include_router(attendance.router)
app.include_router(professor.router)
models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FacultyBase(BaseModel):
    FacultyID: int
    FacultyName: str
    Department: str

class CourseBase(BaseModel):
    Course_code: str
    CourseName: str
    instructor_name:str
    room:str
    credit: int
    level: int
    term: int
    start_date: str
    start_time: str
    end_time: str
    recurrence_pattern: str

class EnrollmentBase(BaseModel):
    StudentID: str
    Course_code: str
    EnrollmentDate: str

class GradeBase(BaseModel):
    GradeID: int
    Grade: str

class VideoFileBase(BaseModel):
    VideoID: int
    StudentID: int
    FileName: str
    FilePath: str
    UploadDate: str

class AttendancesBase(BaseModel):
    StudentID:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
async def root():
    return {"message": "Hello World!!!!!"}

@app.post("/Faculty/",status_code=status.HTTP_201_CREATED)
async def create_faculty(faculty: FacultyBase,db:db_dependency):
    db_user = models.Faculty(**faculty.dict())
    db.add(db_user)
    db.commit()
    
@app.post("/Course/",status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseBase,db:db_dependency):
    # ฟังก์ชันนี้ใช้สำหรับสร้างข้อมูลรายวิชาใหม่ในฐานข้อมูล
    existing_course = db.query(models.Course).filter(
    or_(models.Course.Course_code == course.Course_code,
        models.Course.CourseName == course.CourseName)).first()
    if existing_course:
        # ถ้ารายวิชามีอยู่แล้ว จะส่ง HTTP 404 พร้อมข้อความ "Course already exists"
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course already exists")
    db_user = models.Course(**course.dict())
    db.add(db_user)
    db.commit()
    
@app.post("/Enrollment/",status_code=status.HTTP_200_OK)
async def create_enrollment(enrollment: EnrollmentBase,db:db_dependency,current_user: Annotated[dict,Depends(auth.get_current_user)]):
    # ฟังก์ชันนี้ใช้สำหรับสร้างข้อมูลการลงทะเบียนเรียนใหม่ในฐานข้อมูล
    existing_enrollment = db.query(models.Enrollment).filter(models.Enrollment.Course_code== enrollment.Course_code,models.Enrollment.StudentID==enrollment.StudentID).first()
    if existing_enrollment:
        # ถ้านักเรียนลงทะเบียนเรียนในรายวิชานี้แล้ว จะส่ง HTTP 406 พร้อมข้อความ "Already registered"
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Already registered")
    result = db.query(models.Course.recurrence_pattern).filter(models.Course.Course_code == enrollment.Course_code).all()
    recurrence_patterns = [row.recurrence_pattern for row in result]
    recurrence_patterns_str = ', '.join(recurrence_patterns)
    db_enrollment = models.Enrollment(**enrollment.dict())
    db.add(db_enrollment)
    db.commit()
    start = datetime.strptime("2024-01-15", "%Y-%m-%d")
    end = datetime.strptime("2024-05-31", "%Y-%m-%d")
    current_date = start
    while current_date <= end:
        if current_date.strftime("%A") == recurrence_patterns_str:
            db_Attendance = models.Attendance(AttendanceID=0,StudentID=enrollment.StudentID,Course_code=enrollment.Course_code,Date=current_date.strftime("%Y-%m-%d"),Status='NotYet')
            db.add(db_Attendance)
            db.commit()
        current_date += timedelta(days=1)
    # ส่ง HTTP 201 พร้อมข้อความ "Created"
    raise HTTPException(201,detail="Created")
    
@app.post("/Grade/",status_code=status.HTTP_201_CREATED)
async def create_grade(grade: GradeBase,db:db_dependency):
    db_user = models.Grade(**grade.dict())
    db.add(db_user)
    db.commit()
    
@app.post('/schedule',status_code=status.HTTP_200_OK)
async def get_attendance(data:AttendancesBase,db:db_dependency):
    attendances = db.query(models.Attendance).options(joinedload(models.Attendance.course_detail)).filter(models.Attendance.StudentID == data.StudentID).all()
    return attendances

@app.delete("/Course/{student_id}/{course_code}")
async def delete_enrollment_by_studentid_course_code(db:db_dependency, student_id:int, course_code:str):
    # ลบข้อมูลในตาราง enrollment ที่มี student_id และ course_code ตรงกับที่ระบุ
    db.query(models.Enrollment).filter(
        models.Enrollment.StudentID == student_id,
        models.Enrollment.Course_code == course_code
    ).delete()
    db.query(models.Attendance).filter(
        models.Attendance.StudentID == student_id,
        models.Attendance.Course_code == course_code
        ).delete()
    # ยืนยันการเปลี่ยนแปลง
    db.commit()

#uvicorn app.main:app --reload
#env\Scripts\activate