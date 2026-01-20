import requests
import time
from datetime import datetime, timedelta
import json
import logging
import winsound # Para emitir som alerta

# ==============================================================================
# CONFIGURAÇÕES -- (PRESERVADAS)
# ==============================================================================
TELEGRAM_BOT_TOKEN = "SEU_TOKEN_AQUI"
TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"

# Intervalo entre verificações completas (em segundos)
INTERVALO_VERIFICACAO = 5  # 10 segundos (Modo Turbo)

# Pausa entre cada requisição para não travar a conexão (em segundos)
DELAY_ENTRE_REQUISICOES = 0.3

# Dias para verificar à frente (Ex: verificar os próximos 30 dias)
DIAS_PARA_VERIFICAR = 12

# Ative para ver TODAS as respostas no terminal (True/False)
DEBUG_MODE = True

# ==============================================================================

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')

def enviar_telegram(mensagem):
    """Envia notificação para o Telegram."""
    if TELEGRAM_BOT_TOKEN == "SEU_TOKEN_AQUI":
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

    for i in range(DIAS_PARA_VERIFICAR):
        data_verificacao = hoje + timedelta(days=i)
        data_str = data_verificacao.strftime("%Y-%m-%d")
        data_br = data_verificacao.strftime("%d/%m/%Y")

        turnos = ["MANHA", "TARDE"]

        for turno in turnos:
            payload = {
                "data": data_str,
                "turno": turno
            }

            try:
                time.sleep(DELAY_ENTRE_REQUISICOES) 
                
                # Usamos 'session.post' em vez de 'requests.post' (mantém a conexão viva)
                response = session.post(url, json=payload, timeout=30)

                if response.status_code == 200:
                    dados = response.json()
                    
                    if dados and isinstance(dados, list) and len(dados) > 0:
                        msg = f"✅ **VAGA ENCONTRADA!**\n📅 Data: *{data_br}*\n⏰ Turno: *{turno}*\n🔗 [Acesse Agora](https://juntamedica.rn.gov.br/)"
                        logging.info(msg)
                        vagas_encontradas.append(msg)
                        enviar_telegram(msg)
                        
                        try:
                            winsound.Beep(1000, 1000)
                            winsound.Beep(1500, 1000)
                            winsound.Beep(1000, 1000)
                        except:
                            pass
                    else:
                        if DEBUG_MODE:
                            logging.info(f"🔎 {data_br} ({turno}) -> Status: {response.status_code} | Vz")
                
                elif response.status_code == 405:
                    logging.error("Erro 405: API Incorreta.")
                    return 
                
                elif response.status_code >= 500:
                    logging.warning(f"⚠️ Instabilidade ({response.status_code}) em {data_br}")
                
                else:
                    logging.warning(f"⚠️ Erro inesperado ({response.status_code}) para {data_br}.")

            except requests.exceptions.SSLError:
                logging.warning(f"⚠️ Erro SSL (Conexão Recusada) em {data_br}")
            except requests.exceptions.ConnectionError:
                logging.warning(f"⚠️ Timeout/Queda em {data_br}")
            except Exception as e:
                logging.error(f"❌ Erro: {e}")

    if not vagas_encontradas:
        pass # Silencioso para não poluir, já tem o log de início

def main():
    logging.info("🤖 Monitor Junta Médica - V2.0 (Persistent + Heartbeat)")
    
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
        
        logging.info(f"⏳ Aguardando {INTERVALO_VERIFICACAO}s...")
        time.sleep(INTERVALO_VERIFICACAO)

if __name__ == "__main__":
    main()
