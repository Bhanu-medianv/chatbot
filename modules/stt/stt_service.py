from deepgram import DeepgramClient
from dotenv import load_dotenv
import os


load_dotenv()


class SttService:

    def __init__(self):
        api_key = os.getenv("DEEPGRAM_API_KEY")

        if not api_key:
            raise ValueError(
                "DEEPGRAM_API_KEY is not configured"
            )

        self.client = DeepgramClient(
            api_key=api_key
        )


    def speech_to_text(self, audio: bytes):

        response = self.client.listen.v1.media.transcribe_file(
            request=audio,
            model="nova-3",
            smart_format=True,
            language="en",
        )

        transcript = (
            response.results
            .channels[0]
            .alternatives[0]
            .transcript
        )
        print('this is the transcribe' , transcript)
        return transcript