# chatbot/views.py

import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

import os
from dotenv import load_dotenv  


load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

@csrf_exempt
@api_view(["POST"])
def chat_api(request):
    message = request.data.get("message", "")
    msg = message.lower()

    # 🧑‍💼 Customer Support
    if "customer support" in msg or "support" in msg:
        return Response({
            "type": "text",
            "reply": "📞 Contact support: +91-9876543210"
        })

    elif "login" in msg or "register" in msg:
        return Response({
            "type": "text",
            "reply": "🔐 Login here: /login"
        })

    elif "discount" in msg:
        return Response({
            "type": "text",
            "reply": "💰 20% discount available!"
        })

    elif "offer" in msg:
        return Response({
            "type": "text",
            "reply": "🎁 Buy 1 Get 1 Free!"
        })

    elif "delivery" in msg:
        return Response({
            "type": "text",
            "reply": "🚚 Delivered within 24 hours"
        })

    elif "payment" in msg:
        return Response({
            "type": "text",
            "reply": "💳 UPI, Card, COD available"
        })

    elif "service" in msg:
        return Response({
            "type": "text",
            "reply": "🛠 Farming, organic delivery"
        })

    # 🤖 AI fallback
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": "llama3",
            "prompt": f"Reply shortly: {message}",
            "stream": False
        })

        res.raise_for_status()
        data = res.json()

        return Response({
            "type": "text",
            "reply": data.get("response", "No reply")
        })

    except requests.exceptions.RequestException as e:
        return Response({
            "type": "text",
            "reply": f"⚠️ Ollama error: {str(e)}"
        })