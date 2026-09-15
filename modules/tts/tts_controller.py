from fastapi import APIRouter, Query
from fastapi.responses import Response

from .tts_service import TtsService


router = APIRouter(
    prefix="/tts",
    tags=["TTS"],
)

tts_service = TtsService()


@router.get("/audio")
async def generate_audio(
    text: str = Query(
        ...,
        description="Text to convert into speech",
        examples=["Hello, how can I help you today?"],
    ),
    voiceName: str = Query(
        ...,
        description="Deepgram voice model",
        examples=["flux-hannah-en"],
    ),
):
    audio = tts_service.text_to_speech(
        text=text,
        voice=voiceName,
    )

    return Response(
        content=audio,
        media_type="audio/wav",
        headers={
            "Content-Length": str(len(audio)),
            "Content-Disposition": 'inline; filename="speech.wav"',
        },
    )