import boto3
import os
from datetime import datetime
import uuid

TABLE_DYNAMO_PETS = os.getenv('DYNAMODB_TABLE_PETS')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(TABLE_DYNAMO_PETS)

def get_pets():
    response = table.scan()

    return response.get('Items', None)

def get_pet_by_id(id):
    
    print("petID", id)
    response = table.get_item(Key={'id': id})
    print("Response pet", response)
    return response.get('Item', None)

def get_pet_by_name_and_breed(name, breed):

    response = table.query(
        IndexName='NameIndex',
        KeyConditionExpression=boto3.dynamodb.conditions.Key('nome').eq(name)
    )
    print("Resposta Query", response)
    for pet in response.get('Items', None):
        print("to dentro da iteração")
        if pet['raça'] == breed:
            print(pet)
            return pet
        
    return None


def insert_pet(name, specie,breed, age):

    response = table.put_item(Item={
        'id': str(uuid.uuid4()),  # Gera um UUID para o id
        'nome': name,
        'especie': specie,
        'raça': breed,
        'idade': age,
        'disponivel': True,
    })
    return response