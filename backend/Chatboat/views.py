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

    # 🔐 Login/Register
    elif "login" in msg or "register" in msg:
        return Response({
            "type": "text",
            "reply": "🔐 Login here: /login"
        })

    # 💰 Discounts
    elif "discount" in msg:
        return Response({
            "type": "text",
            "reply": "💰 20% discount available!"
        })

    # 🎁 Offers
    elif "offer" in msg:
        return Response({
            "type": "text",
            "reply": "🎁 Buy 1 Get 1 Free!"
        })

    # 🚚 Delivery
    elif "delivery" in msg:
        return Response({
            "type": "text",
            "reply": "🚚 Delivered within 24 hours"
        })

    # 💳 Payment
    elif "payment" in msg:
        return Response({
            "type": "text",
            "reply": "💳 UPI, Card, COD available"
        })

    # 🛠 Services
    elif "service" in msg:
        return Response({
            "type": "text",
            "reply": "🛠 Farming, organic delivery"
        })

    # 🤖 Ollama AI
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": "llama3",
            "prompt": f"Reply shortly: {message}",
            "stream": False
        })

        data = res.json()

        return Response({
            "type": "text",
            "reply": data.get("response", "No reply")
        })

    except:
        return Response({
            "type": "text",
            "reply": "⚠️ Ollama not running"
        })