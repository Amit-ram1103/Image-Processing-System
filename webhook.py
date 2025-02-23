import requests

def send_webhook_notification(request_id):
    webhook_url = "YOUR_WEBHOOK_URL"
    payload = {"request_id": request_id, "status": "Completed"}
    requests.post(webhook_url, json=payload)
