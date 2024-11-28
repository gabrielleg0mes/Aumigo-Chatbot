import boto3
import os
from datetime import datetime
import uuid

from services.dynamo.pets import get_pet_by_id
from services.dynamo.user import get_user_by_id

DYNAMODB_TABLE_REQUEST_ADOPT = os.getenv('DYNAMODB_TABLE_REQUEST_ADOPT')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_REQUEST_ADOPT)

def insert_adopt_solicitation(id_pet, phone, id_user):

    pet = get_pet_by_id(id_pet)
    user = get_user_by_id(id_user)

    if not pet or not user:
        return None

    response = table.put_item(Item={
        'id': str(uuid.uuid4()),  # Gera um UUID para o id
        'pet': pet,
        'user': user,
        'dataCriacao': datetime.now().isoformat(),
        'status': 'Pendente',
    })
    return response

def get_adopt_solicitations():

    response = table.scan()

    return response.get('Items', None)
