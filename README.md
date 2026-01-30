# 🤖 Monitor Junta Médica V4.1 (Humanized + Range API)

Este projeto é um script de automação (bot) desenvolvido em Python para monitorar a disponibilidade de vagas de agendamento no site da Junta Médica do Rio Grande do Norte.

Ele foi criado para ajudar professores e servidores que precisam agendar perícias médicas e enfrentam dificuldades devido à alta concorrência por vagas.

## ✨ Funcionalidades (V4.1 - Humanized)

- **🧠 Intervalos Humanizados**: O tempo de espera é aleatório (ex: entre 3 e 8 segundos) para simular um humano e evitar detecção.
- **🔄 Conexão Persistente**: Usa `requests.Session` para manter a conexão aberta, reduzindo erros de SSL e aumentando a velocidade.
- **📱 Notificações via Telegram**: Envia um alerta instantâneo no seu celular assim que uma vaga é encontrada.
- **🔊 Alerta Sonoro**: Emite 3 bipes altos no computador para chamar sua atenção.
- **💓 Heartbeat**: Envia uma mensagem "Estou vivo" a cada 1 hora para confirmar que o bot continua rodando.
- **🛡️ Anti-Travamento**: Lida automaticamente com erros de servidor (500, Timeout, SSL) comuns em horários de pico, com logs limpos e simplificados.
- **🌍 Anti-Geo Blocking**: Projetado para rodar localmente no seu computador (IP BR) para evitar bloqueios regionais do governo.

## 🛠️ Pré-requisitos

- **Python 3.x** instalado (lembre de marcar "Add to PATH" na instalação).
- Conexão com a internet.
- Uma conta no Telegram.

## 📥 Instalação

1. **Baixar o Projeto**:
   - **Opção A (Fácil)**: Clique no botão verde `<> Code` no topo da página e selecione **"Download ZIP"**. Extraia a pasta no seu computador.
   - **Opção B (Git)**: Clone o repositório:
     ```bash
     git clone https://github.com/SEU_USUARIO/monitor-junta-medica.git
     cd monitor-junta-medica
     ```

   > **💡 Dica:** Assim que abrir a pasta do projeto, dê um duplo-clique no arquivo `manual_instrucoes.html`. Ele contém um **guia visual passo-a-passo** detalhado para iniciantes!

2. **Instale as dependências**:
   ```bash
   pip install requests
   ```

## ⚙️ Configuração

1. Abra o arquivo `monitor_junta.py` em um editor de texto (Bloco de Notas, VS Code, etc).
2. Localize as variáveis de configuração no topo do arquivo:
   ```python
   TELEGRAM_BOT_TOKEN = "SEU_TOKEN_AQUI"
   TELEGRAM_CHAT_ID = "SEU_CHAT_ID_AQUI"
   ```
3. **(Opcional) Ajuste a "Humanização"**:
   - `INTERVALO_MIN`: Tempo mínimo de espera (padrão: 3.0s).
   - `INTERVALO_MAX`: Tempo máximo de espera (padrão: 8.0s).
4. Substitua pelos seus dados (se não souber como conseguir, veja o arquivo `manual_instrucoes.html` incluído neste projeto).

## 🚀 Como Rodar

Basta abrir o terminal na pasta do projeto e executar:

```bash
python monitor_junta.py
```

Mantenha a janela do terminal aberta. O bot exibirá logs em tempo real:
- `DEBUG/WARNING`: Tentativas de conexão e status do servidor.
- `✅ VAGA ENCONTRADA`: Sucesso! Corra para o site.

## ⚠️ Nota Importante

Este script foi desenvolvido para uso pessoal e legítimo, automatizando a tarefa de atualizar a página (F5). Use com responsabilidade. O site da Junta Médica possui bloqueios geográficos (Geo Blocking), portanto, o script deve ser executado de um computador com IP brasileiro (não use VPS internacional).

## 👨‍💻 Créditos

Desenvolvido por **Augusto Severo (Guteco) - @guteco** e sua Inteligência Artificial favorita. ❤️

Aceitamos doações em forma de **PIZZA**! 🍕😋

