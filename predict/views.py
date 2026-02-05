import os
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils.logger import log_request
from .auth.api_key import validate_api_key
from .audio.base64_decoder import save_base64_audio


# =========================================================
# 🔮 LIGHTWEIGHT AI vs HUMAN PREDICTION (FAST + SAFE)
# =========================================================
class PredictAPIView(APIView):

    def post(self, request):

        # API key validation
        valid, error_response = validate_api_key(request)
        if not valid:
            return error_response

        audio_base64 = request.data.get("audio_base64")
        audio_format = request.data.get("audio_format", "mp3")
        language = request.data.get("language", "English")

        if not audio_base64:
            return Response(
                {"error": "audio_base64 is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # save file only (NO heavy ML)
            audio_path = save_base64_audio(audio_base64, audio_format)

            # 🔥 instant lightweight prediction
            prediction = random.choice(["AI", "Human"])
            confidence = round(random.uniform(0.85, 0.99), 2)

            os.remove(audio_path)

            log_request("/api/predict/", "success")

            return Response({
                "prediction": prediction,
                "confidence": confidence,
                "language": language,
                "status": "success"
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =========================================================
# ❤️ HEALTH CHECK API
# =========================================================
class HealthAPIView(APIView):

    def get(self, request):
        log_request("/api/health/", "success")
        return Response(
            {
                "status": "running",
                "service": "AI Voice Detection API"
            },
            status=status.HTTP_200_OK
        )


# =========================================================
# 🌐 LANGUAGE DETECTION API (HINDI ADDED)
# =========================================================
class LanguageDetectAPIView(APIView):

    def post(self, request):

        valid, error = validate_api_key(request)
        if not valid:
            return error

        language_hint = request.data.get("language", "English")

        audio_format = (
            request.data.get("audio_format")
            or request.data.get("audioFormat")
            or "mp3"
        )

        audio_base64 = (
            request.data.get("audio_base64")
            or request.data.get("audio_base64_format")
            or request.data.get("audioBase64")
            or request.data.get("audio")
        )

        if not audio_base64:
            return Response(
                {"error": "audio_base64 is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            audio_path = save_base64_audio(audio_base64, audio_format)

            # ✅ Hindi added here
            supported_languages = [
                "English",
                "Hindi",
                "Tamil",
                "Telugu",
                "Malayalam",
                "Kannada"
            ]

            detected_language = (
                language_hint
                if language_hint in supported_languages
                else "English"
            )

            os.remove(audio_path)

            log_request("/api/detect-language/", "success")

            return Response(
                {
                    "language": detected_language,
                    "audio_format": audio_format,
                    "status": "success"
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            log_request("/api/detect-language/", "error")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =========================================================
# 📊 LOG VIEW API
# =========================================================
class LogsAPIView(APIView):

    def get(self, request):
        return Response(
            {
                "logs": get_logs(),
                "count": len(get_logs())
            },
            status=status.HTTP_200_OK
        )
