from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime
import yt_dlp
import tempfile
import asyncio
from concurrent.futures import ThreadPoolExecutor
import shutil

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Thread pool for yt-dlp operations
executor = ThreadPoolExecutor(max_workers=3)

# Define Models
class StatusCheck(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StatusCheckCreate(BaseModel):
    client_name: str

class YouTubeDownloadRequest(BaseModel):
    url: str
    format: str = "mp3"  # mp3, wav, m4a, flac, ogg
    quality: str = "high"  # high, medium, low

class DownloadResponse(BaseModel):
    success: bool
    message: str
    file_path: Optional[str] = None
    title: Optional[str] = None

# Quality mappings
QUALITY_MAPPING = {
    "high": "bestaudio",
    "medium": "bestaudio[abr<=128]",
    "low": "bestaudio[abr<=64]"
}

def download_youtube_audio(url: str, format: str, quality: str, output_path: str) -> dict:
    """Download YouTube audio using yt-dlp"""
    try:
        # Configure yt-dlp options
        ydl_opts = {
            'format': QUALITY_MAPPING.get(quality, "bestaudio"),
            'extractaudio': True,
            'audioformat': format,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info first to get the title
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown')
            
            # Download the audio
            ydl.download([url])
            
            # Find the downloaded file
            expected_filename = f"{title}.{format}"
            file_path = os.path.join(output_path, expected_filename)
            
            # Sometimes yt-dlp modifies filenames, so let's find the actual file
            for file in os.listdir(output_path):
                if file.endswith(f'.{format}'):
                    file_path = os.path.join(output_path, file)
                    break
            
            return {
                'success': True,
                'message': 'Download completed successfully',
                'file_path': file_path,
                'title': title
            }
    except Exception as e:
        return {
            'success': False,
            'message': f'Download failed: {str(e)}',
            'file_path': None,
            'title': None
        }

# Add your routes to the router instead of directly to app
@api_router.get("/")
async def root():
    return {"message": "YouTube Audio Downloader API"}

@api_router.post("/download", response_model=DownloadResponse)
async def download_audio(request: YouTubeDownloadRequest):
    """Download audio from YouTube URL"""
    try:
        # Validate YouTube URL
        if 'youtube.com' not in request.url and 'youtu.be' not in request.url:
            raise HTTPException(status_code=400, detail="Please provide a valid YouTube URL")
        
        # Create temporary directory for this download
        temp_dir = tempfile.mkdtemp()
        
        # Run yt-dlp in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor, 
            download_youtube_audio, 
            request.url, 
            request.format, 
            request.quality, 
            temp_dir
        )
        
        if result['success']:
            return DownloadResponse(**result)
        else:
            # Clean up temp directory on failure
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise HTTPException(status_code=400, detail=result['message'])
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@api_router.get("/download-file/{file_id}")
async def download_file(file_id: str):
    """Serve the downloaded audio file"""
    try:
        # In a real implementation, you'd store file paths in database
        # For now, we'll assume the file_id contains the full path
        file_path = file_id.replace("__", "/")  # Simple encoding
        
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            return FileResponse(
                path=file_path,
                filename=filename,
                media_type='application/octet-stream'
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving file: {str(e)}")

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.dict()
    status_obj = StatusCheck(**status_dict)
    _ = await db.status_checks.insert_one(status_obj.dict())
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find().to_list(1000)
    return [StatusCheck(**status_check) for status_check in status_checks]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    executor.shutdown(wait=True)
