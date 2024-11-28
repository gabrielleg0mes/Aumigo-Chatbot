import boto3
import logging
import json

logger = logging.getLogger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LexSessions') 

def carregar_sessao(usuario_id):
    """Carregar estado da sessão do DynamoDB."""
    try:
        response = table.get_item(Key={'SessionId': usuario_id})
        if 'Item' in response:
            logger.info(f"Sessão carregada para o usuário {usuario_id}: {response['Item']}")
            return response['Item'].get('sessionAttributes', {})
        else:
            logger.info(f"Nenhuma sessão existente encontrada para o usuário {usuario_id}.")
            return {}
    except Exception as e:
        logger.error(f"Erro ao carregar a sessão do DynamoDB: {str(e)}")
        return {}


def salvar_sessao(usuario_id, atributos_sessao):
    """Salvar estado da sessão no DynamoDB."""
    try:
        table.put_item(Item={
            'SessionId': usuario_id,
            'sessionAttributes': atributos_sessao
        })
        logger.info(f"Sessão salva para o usuário {usuario_id}: {atributos_sessao}")
    except Exception as e:
        logger.error(f"Erro ao salvar a sessão no DynamoDB: {str(e)}")