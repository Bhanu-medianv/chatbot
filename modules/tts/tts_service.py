
import os

from dotenv import load_dotenv
from deepgram import DeepgramClient


load_dotenv()


VOICES = [
    "flux-hannah-en",
    "flux-kit-en",
    "flux-alexis-en",
    "flux-cliff-en",
    "flux-sienna-en",
    "flux-cole-en",
    "flux-brooke-en",
    "flux-colin-en",
    "flux-gemma-en",
    "flux-haley-en",
    "flux-heather-en",
    "flux-miles-en",
    "flux-sean-en",
    "flux-bree-en",
    "flux-brittany-en",
    "flux-bruce-en",
    "flux-conor-en",
    "flux-donovan-en",
    "flux-drew-en",
    "flux-elise-en",
    "flux-jack-en",
    "flux-kai-en",
    "flux-kelsey-en",
    "flux-maeve-en",
    "flux-marcelo-en",
    "flux-marcus-en",
    "flux-meena-en",
    "flux-meghan-en",
    "flux-naveen-en",
    "flux-paige-en",
    "flux-priya-en",
    "flux-rufus-en",
    "flux-sharon-en",
    "flux-tanner-en",
    "flux-wade-en",
    "flux-wes-en",
]


class TtsService:

    def __init__(self):
        api_key = os.getenv("DEEPGRAM_API_KEY")

        if not api_key:
            raise ValueError(
                "DEEPGRAM_API_KEY is not configured"
            )

        self.client = DeepgramClient(
            api_key=api_key
        )

    def text_to_speech(self, text: str, voice: str) -> bytes:
        if not text:
            raise ValueError("Text is required")

        if not voice:
            raise ValueError("Voice is required")

        if voice not in VOICES:
            raise ValueError(f"Invalid voice: {voice}")

        print("Text:", text)
        print("Voice:", voice)

        try:
            response = (
                self.client
                .speak
                .v2
                .audio
                .generate(
                    text=text,
                    model=voice,
                    encoding="linear16",
                    container="wav",
                )
            )

            # Deepgram returns a generator directly
            chunks = []

            for chunk in response:
                if chunk:
                    chunks.append(chunk)

            audio = b"".join(chunks)

            print("Total audio bytes:", len(audio))

            if not audio:
                raise RuntimeError(
                    "Deepgram returned no audio data"
                )

            return audio

        except Exception as error:
            print("Deepgram TTS Error:", error)
            raise