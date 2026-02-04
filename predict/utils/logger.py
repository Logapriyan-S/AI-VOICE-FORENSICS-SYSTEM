from datetime import datetime

# In-memory log store (no DB)
API_LOGS = []


def log_request(endpoint, status):
    API_LOGS.append({
        "endpoint": endpoint,
        "status": status,
        "time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

    # Keep only last 50 logs
    if len(API_LOGS) > 50:
        API_LOGS.pop(0)


def get_logs():
    return API_LOGS
