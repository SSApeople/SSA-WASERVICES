


import requests

# Datos necesarios
app_id = "486109581181818"
app_secret = "bc9492e11a7f17d0808fe98e95d59546"
user_access_token = "EAAG6HTTog3oBO3ZAPwE2kV7hb7ybqDH0xd6cXaYrsJ7ZBGIF0lbMatL9hGoHQs8OJWMsNBS7ZBv2djSZA9ksLJ8ZAmgHZBOzQX9TZAeIfgwb81CsK30CHGZCMRgV2W65XJ02MZBak6bu6pMfdQ6DUdugNuq0zjM5QNa1k72mcIKOCQB6M7Iqd3uqNB8GZCCkrIQ4oNjc9boDCP5Dd5H50W1QgPfayLXk0ZD"

# URL para generar un token de acceso largo (permanente)
url = f"https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={user_access_token}"

# Realizar la solicitud
response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    long_lived_token = data.get('access_token')
    print("Token de acceso prolongado:", long_lived_token)
else:
    print("Error al generar el token:", response.json())