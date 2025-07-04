import requests
import time

# URL de tu app Streamlit
URL = "https://santifederico-santa-maria-app-pssjxi.streamlit.app/"

# Intervalo entre pings (por ejemplo, cada 20 minutos)
INTERVALO = 20 * 60  

while True:
    try:
        r = requests.get(URL)
        print(f"[{time.ctime()}] Ping enviado - Status: {r.status_code}")
    except Exception as e:
        print(f"Error al hacer ping: {e}")
    time.sleep(INTERVALO)