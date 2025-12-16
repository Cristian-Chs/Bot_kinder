import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

VERIFY_TOKEN = "miverifytoken"  # Puedes cambiarlo
WHATSAPP_TOKEN = "EAA8H2l4cIUIBQNkuBxOINEZBZCS56MHokdc4LYZBqscYVGQCc6M6gCkxYQZAvE0x4AuYI4jhHcStwLT6BEZCY4o7wPZCtlaGuFDEDDuir7IsamqaP3ziZCSoIJlBdDawDMZB57OyMQFRy6hsB2eVLsFHZBSBqUdoxcYysa2eOU6MMkCj84ffqgnfTrE05nidiqdJ4zU2vRvaLYZBUCGhKOZBOH4V4Q7klHZCK4uaSc1f3NeuRmtqM0cMwtvJ9dNmGzxv2gywVqZAKi1eCsKYVhzzpdZAE8"
WHATSAPP_PHONE_ID = "875066875686949"

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
