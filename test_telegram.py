import requests
import logging

# Credenciais (opiadas do monitor_junta.py)
TELEGRAM_BOT_TOKEN = "SEU_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def testar_telegram():
    print(f"📡 Tentando enviar mensagem para Chat ID: {TELEGRAM_CHAT_ID}...")
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": "👋 Olá! Sou eu, o seu Monitor de Vagas.\n\nSe você recebeu isso, está tudo funcionando! 🚀\nAssim que aparecer vaga, eu vou gritar aqui.",
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ SUCESSO! Verifique seu Telegram agora.")
        else:
            print(f"❌ ERRO: O Telegram recusou. Código: {response.status_code}")
            print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"❌ ERRO DE CONEXÃO: {e}")

if __name__ == "__main__":
    testar_telegram()
