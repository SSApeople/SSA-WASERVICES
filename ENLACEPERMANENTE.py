


import requests

# Datos necesarios
app_id = "1210433480051483"
app_secret = "464044a77b07db71278339a11aa5ed65"
user_access_token = "EAARM4gGaSxsBOwpvLM74tZA7WEFeF0hGXBlVZC6NY7fPHvFAWD2nQnZBtZAaWhGqhZCxAW9ZAJXl1ewuVlQZB2ZAmR0j05w0fD2itBvNZAsSiZAc1ttTkMZAogEsj3fZACZC7FcI5p469aL7BiXaK88F9cgOj1noKEiaM6v5iSEYhRTw8BsYCYL5nWcZCfDZCJ4anBzTDcK"

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