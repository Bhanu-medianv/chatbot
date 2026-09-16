from fastapi import APIRouter, UploadFile, File

from .stt_service import SttService


router = APIRouter(
    prefix="/stt",
    tags=["STT"],
)

stt_service = SttService()


@router.post("/audio")
async def speech_to_text(
    audio: UploadFile = File(...),
):
    audio_data = await audio.read()
    
    transcript = await stt_service.speech_to_text(
        audio_data,
    )

    return {
        "success": True,
        "transcript": transcript,
    }