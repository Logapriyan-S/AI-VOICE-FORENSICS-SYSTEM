import librosa
import numpy as np
import warnings


def preprocess_audio(audio_path, sr=16000, duration=10):
    """
    Preprocess audio file and extract features for ML model.

    Args:
        audio_path (str): Path to the audio file
        sr (int): Sample rate for audio loading
        duration (int): Maximum duration in seconds to process

    Returns:
        np.ndarray: Extracted audio features

    Raises:
        Exception: If audio processing fails
    """
    try:
        # Suppress librosa warnings
        warnings.filterwarnings("ignore")

        # Load audio
        audio, sample_rate = librosa.load(
            audio_path,
            sr=sr,
            duration=duration,
            res_type="kaiser_fast"
        )

        # Validate audio
        if audio is None or len(audio) == 0:
            raise Exception("Audio file is empty or could not be loaded")

        # MFCC features
        mfccs = librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=40
        )

        # Additional spectral features
        spectral_centroid = librosa.feature.spectral_centroid(
            y=audio,
            sr=sample_rate
        )

        spectral_rolloff = librosa.feature.spectral_rolloff(
            y=audio,
            sr=sample_rate
        )

        zero_crossing_rate = librosa.feature.zero_crossing_rate(audio)

        # Combine features into a single vector
        features = np.concatenate([
            np.mean(mfccs, axis=1),
            np.std(mfccs, axis=1),
            [np.mean(spectral_centroid)],
            [np.mean(spectral_rolloff)],
            [np.mean(zero_crossing_rate)]
        ])

        return features

    except Exception as e:
        raise Exception(f"Error preprocessing audio: {str(e)}")
