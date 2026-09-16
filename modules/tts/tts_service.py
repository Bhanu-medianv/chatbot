import os

from dotenv import load_dotenv
from deepgram import DeepgramClient


load_dotenv()


# Raw PCM out, so the browser can start playing before the sentence is finished.
SAMPLE_RATE = 24000


VOICES = [
    "flux-hannah-en", "flux-kit-en", "flux-alexis-en", "flux-cliff-en",
    "flux-sienna-en", "flux-cole-en", "flux-brooke-en", "flux-colin-en",
    "flux-gemma-en", "flux-haley-en", "flux-heather-en", "flux-miles-en",
    "flux-sean-en", "flux-bree-en", "flux-brittany-en", "flux-bruce-en",
    "flux-conor-en", "flux-donovan-en", "flux-drew-en", "flux-elise-en",
    "flux-jack-en", "flux-kai-en", "flux-kelsey-en", "flux-maeve-en",
    "flux-marcelo-en", "flux-marcus-en", "flux-meena-en", "flux-meghan-en",
    "flux-naveen-en", "flux-paige-en", "flux-priya-en", "flux-rufus-en",
    "flux-sharon-en", "flux-tanner-en", "flux-wade-en", "flux-wes-en",
]


class TtsService:

    def __init__(self):
        api_key = os.getenv("DEEPGRAM_API_KEY")

        if not api_key:
            raise ValueError("DEEPGRAM_API_KEY is not configured")

        self.client = DeepgramClient(api_key=api_key)

        # Set once we know which kwargs this account/SDK actually accepts.
        self._raw_pcm_supported = None

    def _validate(self, text: str, voice: str):
        if not text or not text.strip():
            raise ValueError("Text is required")

        if voice not in VOICES:
            raise ValueError(f"Invalid voice: {voice}")

    def _generate(self, text: str, voice: str, raw: bool):
        if raw:
            return self.client.speak.v2.audio.generate(
                text=text,
                model=voice,
                encoding="linear16",
                sample_rate=SAMPLE_RATE,
                container="none",
            )

        return self.client.speak.v2.audio.generate(
            text=text,
            model=voice,
            encoding="linear16",
            container="wav",
        )

    def stream(self, text: str, voice: str):
        """Blocking generator of linear16 chunks.

        Falls back to a WAV container if raw PCM is rejected; the caller strips
        the 44-byte header off the first chunk either way.
        """

        self._validate(text, voice)

        if self._raw_pcm_supported is None:
            try:
                response = self._generate(text, voice, raw=True)
                iterator = iter(response)
                first = next(iterator)

                self._raw_pcm_supported = True

                if first:
                    yield first

                for chunk in iterator:
                    if chunk:
                        yield chunk

                return
            except StopIteration:
                self._raw_pcm_supported = True
                return
            except Exception as error:
                print("Deepgram rejected raw PCM, falling back to WAV:", error)
                self._raw_pcm_supported = False

        for chunk in self._generate(text, voice, raw=self._raw_pcm_supported):
            if chunk:
                yield chunk

    def text_to_speech(self, text: str, voice: str) -> bytes:
        """Full WAV, kept for the old REST route."""

        self._validate(text, voice)

        audio = b"".join(
            chunk for chunk in self._generate(text, voice, raw=False) if chunk
        )
        
        if not audio:
            raise RuntimeError("Deepgram returned no audio data")

        return audio