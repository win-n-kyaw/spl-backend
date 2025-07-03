from fastapi import APIRouter, Response
import requests

router = APIRouter(tags=["Image Proxy"])

@router.get("/image-proxy/{file_id}")
def proxy_image(file_id: str):
    drive_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    
    # Fetch the image using requests (not aiohttp because it's a sync endpoint)
    response = requests.get(drive_url)

    if response.status_code != 200:
        return Response(content="Image access blocked or file not found", status_code=403)

    # You can also inspect response.headers['Content-Type'] if needed
    return Response(content=response.content, media_type="image/jpeg")
