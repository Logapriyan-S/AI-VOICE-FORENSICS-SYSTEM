import os
import requests
import uuid
from django.conf import settings


def download_audio(audio_url):
    """
    Download audio file from URL and save it temporarily.

    Args:
        audio_url (str): URL of the audio file to download

    Returns:
        str: Absolute path to the downloaded audio file

    Raises:
        Exception: If download fails or URL is invalid
    """
    try:
        # Create temporary audio directory
        temp_dir = os.path.join(settings.BASE_DIR, "temp_audio")
        os.makedirs(temp_dir, exist_ok=True)

        # Generate unique filename
        file_name = f"{uuid.uuid4()}.mp3"
        file_path = os.path.join(temp_dir, file_name)

        # HTTP headers for better compatibility
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36"
            )
        }

        # Download audio (streaming)
        response = requests.get(
            audio_url,
            timeout=30,
            stream=True,
            headers=headers
        )
        response.raise_for_status()

        # Write audio to file
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return file_path

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download audio: {str(e)}")

    except Exception as e:
        raise Exception(f"Error processing audio URL: {str(e)}")
