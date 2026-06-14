# app/utils/cloudinary.py

import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

def delete_from_cloudinary(public_id: str):
    if not public_id:
        return None
    return cloudinary.uploader.destroy(public_id)