from fastapi import FastAPI
from fastapi.responses import FileResponse

from modules.stt.stt_controller import router as stt_router
from modules.tts.tts_controller import router as tts_router
from modules.realtime.voice_controller import router as voice_router


app = FastAPI(
    title="Voice AI",
)


# Register routers
app.include_router(stt_router)
app.include_router(tts_router)
app.include_router(voice_router)


@app.get("/")
async def root():
    return FileResponse("static/index.html")