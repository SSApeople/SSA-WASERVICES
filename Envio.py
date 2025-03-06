import requests
import json

# Configuración
ACCESS_TOKEN = "EAAG6HTTog3oBO98BlCwJ4xtPl1ytvgnGYb7DRhuomZBi2Jlb5mqL3v7Q2Hw1ctFaqZCF2CGkXR0lcmvcieYjGXej4BZAVyRYe6ccdw75QYTkLP4NZBu1aizIZCKMQV5speyyvIYcioDn9btFd4CiKmNVZAN0d01VCg2l22McltlekdZAKDPlDJZBlCxG"
PHONE_NUMBER_ID = "557935180732301"
RECIPIENT_PHONE = "+525545886092"
OTP_CODE = "123456"

# URL de la API de WhatsApp Cloud
url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

# Datos del mensaje en formato JSON con un botón de URL
data = {
    "messaging_product": "whatsapp",
    "to": RECIPIENT_PHONE,
    "type": "template",
    "template": {
        "name": "plantilla",  # Asegúrate de que esta plantilla existe en WhatsApp Business Manager
        "language": {"code": "es"},
        "components": [
            {
                "type": "body",
                "parameters": [
                    {"type": "text", "text": OTP_CODE}
                ]
            },
            {
                "type": "button",
                "sub_type": "url",
                "index": 0,
                "parameters": [
                    {"type": "text", "text":  OTP_CODE}
                ]
            }
        ]
    }
}

# Encabezados de la solicitud
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Enviar la solicitud POST
response = requests.post(url, headers=headers, data=json.dumps(data))

# Mostrar la respuesta de la API
print(response.status_code)
print(response.json())
