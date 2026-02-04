import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils.logger import log_request, get_logs
from .auth.api_key import validate_api_key
from .audio.preprocess import preprocess_audio
from .ml.predictor import predict_voice
from .audio.base64_decoder import save_base64_audio


# =========================================================
# 🔮 AI vs HUMAN PREDICTION API (BASE64 – FINAL)
# =========================================================
class PredictAPIView(APIView):

    def post(self, request):

        # 🔐 API key validation
        valid, error_response = validate_api_key(request)
        if not valid:
            log_request("/api/predict/", "unauthorized")
            return error_response

        audio_base64 = request.data.get("audio_base64")
        audio_format = request.data.get("audio_format", "mp3")
        language = request.data.get("language", "English")

        if not audio_base64:
            log_request("/api/predict/", "bad_request")
            return Response(
                {"error": "audio_base64 is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 💾 Save Base64 audio
            audio_path = save_base64_audio(audio_base64, audio_format)

            # 🎵 Preprocess audio
            features = preprocess_audio(audio_path)

            # 🤖 Predict AI vs Human
            prediction, confidence = predict_voice(features)

            # 🧹 Cleanup
            os.remove(audio_path)

            log_request("/api/predict/", "success")

            return Response(
                {
                    "prediction": prediction,
                    "confidence": confidence,
                    "language": language,
                    "status": "success"
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            log_request("/api/predict/", "error")
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
# 🌐 LANGUAGE HANDLING API (TESTER-COMPATIBLE)
# =========================================================
class LanguageDetectAPIView(APIView):
    def post(self, request):

        valid, error = validate_api_key(request)
        if not valid:
            return error

        language_hint = request.data.get("language", "English")
        audio_format = request.data.get("audio_format", "mp3")
        audio_base64 = request.data.get("audio_base64")

        if not audio_base64:
            return Response(
                {"error": "audio_base64 is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            audio_path = save_base64_audio(audio_base64, audio_format)

            supported_languages = [
                "English", "Tamil", "Telugu", "Malayalam", "Kannada"
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
