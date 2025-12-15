import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

VERIFY_TOKEN = "miverifytoken"  # Puedes cambiarlo
WHATSAPP_TOKEN = "EAA8H2l4cIUIBQJe5xdTJUTN9MYbFbhiy9B62a7hXXhbX2y04ZCmFFiIMCgvNcwvEhk9NUm2KsaVYtwCDabmKWMDw0ZBANwZAvK3Evz6QXGGlh2NeV8Khk9NL1cXQCJ0aSZAUbbIQFvcvAh1hTuMkcw1ktAcqrU9lAPdIRl1oScAr8GrOX0Dqms3LSw8ZADmGG4a6hS3ELH0FdFq07S9r14R1M8SCb40OmBOXXZCrZBLaOXZARxe9gFd7uMcwee1AETikLnub5hEwRxAcgFZAAZBAu0NgZDZD"
WHATSAPP_PHONE_ID = "+584246188448"

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "GET":
        # Verificación del webhook con Meta
        if request.GET.get("hub.verify_token") == VERIFY_TOKEN:
            return HttpResponse(request.GET.get("hub.challenge"))
        return HttpResponse("Token inválido", status=403)

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        try:
            message = data["entry"][0]["changes"][0]["value"]["messages"][0]
            sender = message["from"]
            text = message["text"]["body"].strip().lower()

            if text == "hola":
                enviar_mensaje(sender, "Hola, soy un asistente virtual.")
        except Exception as e:
            print("Error:", e)

        return HttpResponse("EVENT_RECEIVED")

def enviar_mensaje(to, message):
    url = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)
