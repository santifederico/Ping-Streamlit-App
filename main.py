# main.py
import os
import requests
import time

# URL de tu aplicación Streamlit
STREAMLIT_APP_URL = os.getenv('STREAMLIT_APP_URL')
# Token de tu bot de Telegram (obtenido de BotFather)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# ID del chat o usuario de Telegram al que enviar el mensaje
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def visit_streamlit_app(url):
    """
    Visita la URL de la aplicación Streamlit para generar tráfico.
    """
    print(f"Intentando visitar la aplicación Streamlit en: {url}")
    try:
        response = requests.get(url, timeout=30) # Aumentar el timeout a 30 segundos
        response.raise_for_status()  # Lanza una excepción para códigos de estado de error (4xx o 5xx)
        print(f"Visita exitosa a la aplicación Streamlit. Código de estado: {response.status_code}")
        return True, f"Visita exitosa. Código de estado: {response.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Error al visitar la aplicación Streamlit: {e}")
        return False, f"Error al visitar la aplicación: {e}"

def send_telegram_message(token, chat_id, message):
    """
    Envía un mensaje al bot de Telegram.
    """
    api_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown' # Puedes usar 'HTML' o 'Markdown'
    }
    print(f"Intentando enviar mensaje a Telegram para chat ID: {chat_id}")
    try:
        response = requests.post(api_url, json=payload, timeout=10) # Aumentar el timeout a 10 segundos
        response.raise_for_status()
        print(f"Mensaje de Telegram enviado exitosamente. Código de estado: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar mensaje a Telegram: {e}")
        return False

def main():
    if not STREAMLIT_APP_URL:
        print("Error: La variable de entorno 'STREAMLIT_APP_URL' no está configurada.")
        return
    if not TELEGRAM_BOT_TOKEN:
        print("Error: La variable de entorno 'TELEGRAM_BOT_TOKEN' no está configurada.")
        return
    if not TELEGRAM_CHAT_ID:
        print("Error: La variable de entorno 'TELEGRAM_CHAT_ID' no está configurada.")
        return

    print("Iniciando el bot de tráfico...")
    success, visit_result_message = visit_streamlit_app(STREAMLIT_APP_URL)

    telegram_message = f"🤖 *Informe del Bot de Tráfico Streamlit*\n\n"
    telegram_message += f"🔗 *URL de la App:* `{STREAMLIT_APP_URL}`\n"

    if success:
        telegram_message += f"✅ *Estado:* Éxito\n"
        telegram_message += f"📝 *Detalles:* {visit_result_message}\n"
    else:
        telegram_message += f"❌ *Estado:* Fallo\n"
        telegram_message += f"📝 *Detalles:* {visit_result_message}\n"

    send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, telegram_message)
    print("Proceso completado.")

if __name__ == "__main__":
    main()