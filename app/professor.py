from typing import Annotated
from urllib.parse import unquote
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from requests import Session
from sqlalchemy import or_,func,case
from sqlalchemy.orm import joinedload,load_only,selectinload
import app.models as models
from .database import engine,SessionLocal

router = APIRouter(
    tags=['professor']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

class Course_Detail(BaseModel):
    course_code:str
    date:str

class ProfessorSubject(BaseModel):
    Professor_name:str


@router.post("/Course/detail",status_code=status.HTTP_200_OK)
async def fetchCourseData(data:Course_Detail,db:db_dependency):
    #db_query_all = db.query(models.Attendance).filter(models.Attendance.Course_code==data.course_code,models.Attendance.Date==data.date).count()
    #db_query_Present = db.query(models.Attendance).filter(models.Attendance.Course_code==data.course_code,models.Attendance.Date==data.date
    #                                                    ,models.Attendance.Status == 'Present').count()
    #db_query_notYet = db.query(models.Attendance).filter(models.Attendance.Course_code==data.course_code,models.Attendance.Date==data.date
    #                                                    ,models.Attendance.Status == 'NotYet').count()
    db_query_all = db.query(models.Attendance).options(selectinload(models.Attendance.student).load_only(models.Student.FirstName,models.Student.LastName)).filter(models.Attendance.Course_code==data.course_code,models.Attendance.Date==data.date).all()
    present = len([user for user in db_query_all if user.Status=='Present'])
    notYet = len([user for user in db_query_all if user.Status=='NotYet'])
    Absent = len([user for user in db_query_all if user.Status=='Absent'])
    Leave = len([user for user in db_query_all if user.Status=='Leave'])
    Late = len([user for user in db_query_all if user.Status=='Late'])
    return {"Students":db_query_all,"status":{"Present":present,"notyet":notYet,"Absent":Absent,"Leave":Leave,"Late":Late}}

@router.post("/Subjects_taught",status_code=status.HTTP_200_OK)
async def FetchProfessorSubject(data:ProfessorSubject,db:db_dependency):
    data_query = db.query(models.Course).filter(models.Course.instructor_name == data.Professor_name).all()
    return data_query

class Report(BaseModel):
    course_code :str

@router.post("/Class_report",status_code=status.HTTP_200_OK)
async def ClassReport(data:Report,db:db_dependency):
    attendance_report = db.query(
        models.Attendance.StudentID,
        func.sum(case((models.Attendance.Status == "NotYet", 1), else_=0)).label("NotYet"),
        func.sum(case((models.Attendance.Status == "Present", 1), else_=0)).label("Present"),
        func.sum(case((models.Attendance.Status == "Leave", 1), else_=0)).label("Leave"),
        func.sum(case((models.Attendance.Status == "Late", 1), else_=0)).label("Late")
    ).filter(
        models.Attendance.Course_code == data.course_code
    ).group_by(
        models.Attendance.StudentID
    ).all()

    # สร้าง list เพื่อเก็บข้อมูล
    report_list = [
        {
            "StudentID": student_id,
            "NotYet": not_yet,
            "Present": present,
            "Leave": leave,
            "Late": late
        }
        for student_id, not_yet, present, leave, late in attendance_report
    ]

    return report_list
    