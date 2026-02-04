import os
from django.http import JsonResponse

# Read API key from environment variable
# Fallback to default key if not set
API_KEY = os.getenv("API_KEY", "test123")


def validate_api_key(request):
    api_key = request.headers.get("x-api-key")

    if not api_key:
        return False, JsonResponse(
            {"error": "x-api-key header missing"},
            status=401
        )

    if api_key != API_KEY:
        return False, JsonResponse(
            {"error": "Invalid API key"},
            status=401
        )

    return True, None
