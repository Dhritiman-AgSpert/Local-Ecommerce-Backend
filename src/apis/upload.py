import boto3
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from PIL import Image
from io import BytesIO
import os
import uuid

from .. import models, database, schema, config
from .auth import get_current_user

router = APIRouter()

s3 = boto3.client(
    's3', 
    region_name='ap-south-1', 
    aws_access_key_id=config.settings.AWS_ACCESS_KEY_ID, 
    aws_secret_access_key=config.settings.AWS_SECRET_ACCESS_KEY
)

@router.post("/image/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(database.get_db), _: schema.User = Depends(get_current_user)):
    file_content = await file.read()

    # Validate if the file is an image
    try:
        Image.open(BytesIO(file_content))
    except IOError as e:
        raise HTTPException(status_code=400, detail="Invalid image file.") from e
    
    # Generate a random 32 character string for the filename while preserving the extension
    ext = os.path.splitext(file.filename)[1]
    random_filename = f"{uuid.uuid4().hex}{ext}"
    
    print(file.content_type)
    s3.upload_fileobj(BytesIO(file_content), 'hypermaakbucket', random_filename, ExtraArgs={
        'ACL': 'public-read',
        "ContentType": file.content_type
    })
    url = f"{s3.meta.endpoint_url}/hypermaakbucket/{random_filename}"

    img = models.Image(url=url)
    db.add(img)
    db.commit()

    return {"url": url}

# @router.get("/image/{img_id}")
# async def get_image(img_id: int, , db: Session = Depends(database.get_db)):
#     img = db.query(models.Image).filter(models.Image.id == img_id).first()
#     if not img:
#         raise HTTPException(status_code=404, detail="Image not found")
#     return {"name": img.name, "url": img.url}
