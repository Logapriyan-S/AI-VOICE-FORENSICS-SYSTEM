import base64
import uuid
import os
from django.conf import settings


def save_base64_audio(base64_audio, audio_format="mp3"):
    try:
        temp_dir = os.path.join(settings.BASE_DIR, "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)

        audio_bytes = base64.b64decode(base64_audio)

        file_path = os.path.join(
            temp_dir,
            f"{uuid.uuid4()}.{audio_format}"
        )

        with open(file_path, "wb") as f:
            f.write(audio_bytes)

        return file_path

    except Exception as e:
        raise Exception(f"Invalid base64 audio: {str(e)}")
