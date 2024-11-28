import boto3
import json
import logging
from services.dynamo.lex_sessions import carregar_sessao, salvar_sessao

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Cliente do Lex V2
lex_v2_client = boto3.client('lexv2-runtime')

# Configurações do Lex V2
BOT_ID = 'seu-bot-id'
BOT_ALIAS_ID = 'seu-alias-id'
LOCALE_ID = 'pt_BR'

def webhook(event, context):
    """Handler principal do webhook."""
    try:
        # Extrair dados da requisição do Twilio
        body = event.get('body', '{}')
        params = json.loads(body)
        mensagem_usuario = params.get('Body', '')  # Mensagem do usuário
        usuario_id = params.get('From', '')        # Número do usuário

        if not mensagem_usuario or not usuario_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Entrada inválida: falta Body ou From"})
            }

        # Carregar estado da sessão do usuário
        atributos_sessao = carregar_sessao(usuario_id)

        # Enviar mensagem para o Lex V2
        resposta_lex = lex_v2_client.recognize_text(
            botId=BOT_ID,
            botAliasId=BOT_ALIAS_ID,
            localeId=LOCALE_ID,
            sessionId=usuario_id,
            text=mensagem_usuario,
            sessionState={
                "sessionAttributes": atributos_sessao
            }
        )

        # Processar a resposta do Lex
        mensagens_bot = [msg['content'] for msg in resposta_lex.get('messages', [])]
        sessao_atualizada = resposta_lex.get('sessionState', {})
        novos_atributos_sessao = sessao_atualizada.get('sessionAttributes', {})

        # Atualizar a sessão no DynamoDB
        salvar_sessao(usuario_id, novos_atributos_sessao)

        # Retornar resposta para o Twilio
        resposta_twilio = {
            "Body": " ".join(mensagens_bot)
        }

        return {
            "statusCode": 200,
            "body": json.dumps(resposta_twilio)
        }

    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Erro interno no servidor."})
        }
