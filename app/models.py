import uuid
from sqlalchemy import UUID, Date, Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, BIGINT, Time, func, select
from sqlalchemy.orm import relationship,column_property
from .database import Base

class Auth_users(Base):
    __tablename__ = "auth_users"
    
    id = Column(String(36), primary_key=True,default=func.uuid());
    Email = Column(String(255),primary_key=True);
    password = Column(String(255));
    pin = Column(String(6));
    student = relationship("Student", back_populates="auth_users");
    Personnel = relationship("Personnel", back_populates="auth_users");
    Roll = Column(String(10));

class Student(Base):
    __tablename__ = "students"

    StudentID = Column(String(15), primary_key=True);
    FirstName = Column(String(50));
    LastName = Column(String(50));
    fullname = column_property(FirstName + " " + LastName)
    Email = Column(String(50),ForeignKey('auth_users.Email'));
    Degree = Column(Enum('Bachelor','Master','PhD'));
    Year = Column(String(1));
    FacultyName = Column(String(50));
    Department = Column(String(50));
    _isFaceLoginEnable = Column(Boolean,default=False);
    enrollments = relationship("Enrollment", back_populates="student");
    videofiles = relationship("VideoFile", back_populates="student");
    attendances = relationship("Attendance", back_populates="student");
    auth_users = relationship("Auth_users",back_populates="student");

class Personnel(Base):
    __tablename__= "Personnel"
    
    id = Column(String(36), primary_key=True,default=func.uuid());
    FirstName = Column(String(50),primary_key=True);
    LastName = Column(String(50));
    Email = Column(String(50),ForeignKey('auth_users.Email'));
    auth_users = relationship("Auth_users",back_populates="Personnel");

class Faculty(Base):
    __tablename__ = "faculties"

    FacultyID = Column(Integer, primary_key=True)
    FacultyName = Column(String(50))
    Department = Column(String(50))

class Course(Base):
    __tablename__ = "courses"
    Course_id =Column(Integer,primary_key=True,autoincrement=True)
    Course_code = Column(String(8), primary_key=True)
    CourseName = Column(String(70))
    instructor_name = Column(String(100))
    room = Column(String(10))
    credit = Column(Integer)
    level = Column(Integer)
    term = Column(Integer)
    start_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    recurrence_pattern  = Column(String(10))
    late_time = Column(String(3),default=30)
    attendances = relationship("Attendance", back_populates="course_detail")
    course_check = relationship("course_check", back_populates="course_detail")

class Enrollment(Base):
    __tablename__ = "enrollments"

    EnrollmentID = Column(String(36), primary_key=True,default=func.uuid())
    StudentID = Column(BIGINT, ForeignKey('students.StudentID'))
    Course_code = Column(String(7))
    GradeID = Column(Integer)
    EnrollmentDate = Column(Date)
    student = relationship("Student", back_populates="enrollments")

class Grade(Base):
    __tablename__ = "grades"

    GradeID = Column(Integer, primary_key=True)
    Grade = Column(String(50))

class VideoFile(Base):
    __tablename__ = "videofiles"

    VideoID = Column(Integer, primary_key=True)
    StudentID = Column(BIGINT, ForeignKey('students.StudentID'))
    FileName = Column(String(50))
    FilePath = Column(String(50))
    UploadDate = Column(Date)
    student = relationship("Student", back_populates="videofiles")
    
class Attendance(Base):
    __tablename__ = 'attendances'
    
    AttendanceID = Column(Integer, primary_key=True, index=True)
    StudentID = Column(BIGINT, ForeignKey('students.StudentID'))
    Course_code = Column(String(8), ForeignKey('courses.Course_code'))
    Date = Column(Date)
    Status = Column(Enum('Present', 'Absent', 'Leave', 'NotYet', 'Late', name='status_enum'))
    course_detail = relationship("Course", back_populates="attendances")
    student = relationship("Student", back_populates="attendances")
    
class course_check(Base):
    __tablename__ = 'course_check'
    
    id = Column(String(36), primary_key=True,default=func.uuid());
    Course_code = Column(String(8), ForeignKey('courses.Course_code'))
    code = Column(String(6))
    Date = Column(Date)
    course_detail = relationship("Course", back_populates="course_check")