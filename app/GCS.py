import io
import app.models as models
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File
from fastapi.responses import StreamingResponse
from google.cloud import storage
from requests import Session
from .database import SessionLocal
router = APIRouter(
    tags=['GCS']
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]
# กำหนดข้อมูล credentials สำหรับเชื่อมต่อกับ GCS
storage_json='handy-apex-413714-9f4b5359232c.json'
storage_client = storage.Client.from_service_account_json(storage_json)
video = 'face_images_bucket_cpe34'
image_profile = 'picture_profile'

@router.post("/upload/Video/")
async def upload_video(student_id: str,db:db_dependency, video: UploadFile = File(...)):
    # บันทึกรูปภาพไปยัง Google Cloud Storage
    users = db.query(models.Student).filter(models.Student.StudentID == student_id).first()
    blob_name = video.filename
    blob = storage_client.bucket(video).blob(f"{student_id}/{blob_name}")
    blob.upload_from_string(await video.read(), content_type=video.content_type)
    if users:
        users._isFaceLoginEnable = True
        db.commit()
    return {"folder":student_id,"filename": video.filename}

@router.get("/get/image/{image_name}")
async def get_image(image_name: str):
    # ดึงรูปภาพจาก Google Cloud Storage
    blob = storage_client.bucket(video).blob(image_name)
    blob_data = blob.download_as_string()
    return StreamingResponse(io.BytesIO(blob_data), media_type="image/jpeg")

@router.post("/upload/image/")
async def upload_image_profile(Id:str,db:db_dependency,image: UploadFile = File(...)):
    image.filename = Id+'_imageprofile'
    bucket = storage_client.bucket(image_profile).blob(f"{Id}/{image.filename}")
    if bucket.exists():
        bucket.delete()
    bucket.content_type = 'image/jpeg'
    bucket.upload_from_file(image.file)
    image_url = f"https://storage.googleapis.com/{image_profile}/{Id}/{image.filename}"
    return {"message": "Upload successful", "image_url": image_url}