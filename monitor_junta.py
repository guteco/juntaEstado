import requests
import time
from datetime import datetime, timedelta
import json
import logging
import winsound # Para emitir som alerta
import random # Para intervalo aleatório

# ==============================================================================
# CONFIGURAÇÕES -- (PRESERVADAS)
# ==============================================================================
TELEGRAM_BOT_TOKEN = "TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "TELEGRAM_CHAT_ID"

# Intervalo entre verificações completas (em segundos)
# Intervalo ALEATÓRIO entre verificações (para parecer humano)
# Tempo mínimo e máximo em segundos (pode usar ponto, ex: 2.5)
INTERVALO_MIN = 3.0
INTERVALO_MAX = 8.0

# Pausa entre cada requisição para não travar a conexão (em segundos)
DELAY_ENTRE_REQUISICOES = 0.3

# Dias para verificar à frente (Ex: verificar os próximos 30 dias)
DIAS_PARA_VERIFICAR = 30

# Ative para ver TODAS as respostas no terminal (True/False)
DEBUG_MODE = True

# ==============================================================================

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

def enviar_telegram(mensagem):
    """Envia notificação para o Telegram."""
    if TELEGRAM_BOT_TOKEN == "TELEGRAM_BOT_TOKEN":
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    try:
        # Timeout curto para não travar o monitor se o Telegram engasgar
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        logging.error(f"Erro de conexão com Telegram: {e}")

def verificar_vagas(session):
    """Verifica vagas na API da Junta Médica usando uma sessão persistente."""
    url = "https://juntamedica.rn.gov.br/api/horario"
    
    hoje = datetime.now().date()
    vagas_encontradas = []

    logging.info(f"🔄 Iniciando ciclo de verificação ({DIAS_PARA_VERIFICAR} dias)...")

    # NOVAS REGRAS DA API (20/01/2026): Range de datas via GET
    data_inicial = hoje.strftime("%Y-%m-%d")
    data_final_obj = hoje + timedelta(days=DIAS_PARA_VERIFICAR)
    data_final = data_final_obj.strftime("%Y-%m-%d")

    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final
    }

    try:
        # Agora é GET com parâmetros de URL
        response = session.get(url, params=params, timeout=30)
        
        data_br_range = f"{hoje.strftime('%d/%m')} a {data_final_obj.strftime('%d/%m')}"

        if response.status_code == 200:
            dados = response.json()
            
            # Se a lista não estiver vazia, TEM VAGA!
            if dados and isinstance(dados, list) and len(dados) > 0:
                # Como não sabemos o formato exato do objeto novo, convertemos pra string bonita
                dados_str = json.dumps(dados, indent=2, ensure_ascii=False)
                
                msg = f"✅ **VAGA ENCONTRADA!**\n\nO site retornou vagas no período de {data_br_range}!\n\nDados brutos:\n`{dados_str}`\n\n🔗 [Acesse Agora](https://juntamedica.rn.gov.br/)"
                logging.info("\n" + msg)
                enviar_telegram(msg)
                
                try:
                    winsound.Beep(1000, 1000)
                    winsound.Beep(1500, 1000)
                    winsound.Beep(1000, 1000)
                except:
                    pass
            else:
                if DEBUG_MODE:
                    # Log mais limpo: Apenas 1 linha por ciclo
                    logging.info(f"🔎 {data_br_range} -> Status: 200 | Vz (Sem vagas)")
        
        elif response.status_code == 405:
            logging.error("Erro 405: API mudou novamente ou método incorreto.")
        
        elif response.status_code >= 500:
            logging.warning(f"⚠️ Instabilidade ({response.status_code}) - O site está congestionado.")
        
        else:
            logging.warning(f"⚠️ Erro inesperado ({response.status_code}).")

    except requests.exceptions.SSLError:
        logging.warning("⚠️ Erro SSL (Conexão caiu) - Tentando novamente...")
    except requests.exceptions.ConnectionError:
        logging.warning("⚠️ Erro de Conexão/Timeout - O servidor não respondeu.")
    except Exception as e:
        logging.error(f"❌ Erro genérico: {e}")

def main():
    logging.info("🤖 Monitor Junta Médica - V3.0 (Humanized + Range API)")
    
    # ---------------------------------------------------------
    # MELHORIA 1: SESSÃO PERSISTENTE
    # Cria a conexão uma vez e reutiliza (como um telefone fora do gancho)
    # ---------------------------------------------------------
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })

    ultima_batida_coracao = time.time()
    
    # Manda um oi inicial
    enviar_telegram("🤖 **Bot Iniciado!**\nModo Turbo + Conn Persistente Ativados.\nVou te avisar aqui a cada 1h que estou vivo.")

    while True:
        try:
            # ---------------------------------------------------------
            # MELHORIA 4: HEARTBEAT (Sinal de Vida) a cada 1 hora
            # ---------------------------------------------------------
            agora = time.time()
            if agora - ultima_batida_coracao > 3600: # 3600 segundos = 1 hora
                enviar_telegram("💓 **Estou vivo!**\nMonitorando sem parar. Nenhuma vaga encontrada ainda.")
                logging.info("💓 Heartbeat enviado para o Telegram.")
                ultima_batida_coracao = agora

            verificar_vagas(session)
            
        except Exception as e:
            logging.error(f"Erro fatal no loop: {e}")
            # Se a sessão quebrar muito feio, recria
            session = requests.Session()
            session.headers.update({
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
        
        tempo_espera = random.uniform(INTERVALO_MIN, INTERVALO_MAX)
        logging.info(f"⏳ Aguardando {tempo_espera:.2f}s...")
        time.sleep(tempo_espera)

if __name__ == "__main__":
    main()
