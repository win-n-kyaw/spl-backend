import io
import os
import mimetypes
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
from fastapi import UploadFile
from dotenv import load_dotenv

load_dotenv()

GDRIVE_FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")

# Authenticate using service account
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"  

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)

def upload_file_to_drive(upload_file: UploadFile, folder_id: str = GDRIVE_FOLDER_ID) -> str: #type: ignore
    # Read the file content into memory
    file_content = io.BytesIO(upload_file.file.read())

    mime_type = upload_file.content_type or mimetypes.guess_type(upload_file.filename)[0] or "application/octet-stream" #type: ignore

    file_metadata = {
        "name": upload_file.filename,
        "parents": [folder_id],
    }

    media = MediaIoBaseUpload(file_content, mimetype=mime_type)

    uploaded = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    # Make file public
    drive_service.permissions().create(
        fileId=uploaded["id"],
        body={"role": "reader", "type": "anyone"},
    ).execute()

    # Return the public URL
    file_id = uploaded["id"]
    return file_id
