from services.dynamo.user import search_by_phone, insert_user
from utils.lex_utils import generate_lex_response

def verifcacaoCadastro(sessionState, sessionAttributes, slots, intentName):
    phone = slots.get('verificaTelefone', {}).get('value', {}).get('interpretedValue', "Não informado")

    # search for the user in the database
    result = search_by_phone(phone)
    print(len(result))
    print(len(result) > 0)
    if len(result) > 0:
        user = result[0]  # take the first user found
        # update slots with user data
        slots.update({
            'nome': {"value": {"interpretedValue": user.get('name', "Desconhecido")}},
            'e-mail': {"value": {"interpretedValue": user.get('email', "Desconhecido")}},
            'telefone': {"value": {"interpretedValue": user.get('phone', "Desconhecido")}},
            'idade': {"value": {"interpretedValue": user.get('age', "Desconhecido")}}
        })

        sessionAttributes['nome'] = user.get('name')
        sessionAttributes['e-mail'] = user.get('email')
        sessionAttributes['telefone'] = user.get('phone')
        sessionAttributes['idade'] = user.get('age')
        sessionAttributes['userId'] = user.get('id')

        sessionState['intent']['slots'] = slots  # update slots in sessionState

        response_message = "Cadastro encontrado."
    else:
        response_message = "Seu cadastro não foi encontrado. Digite 'Recomeçar' para reiniciar a conversa!"

    return generate_lex_response(
            intentName=intentName,
            sessionState=sessionState,
            sessionAttributes=sessionAttributes,
            message=response_message,
            state="Fulfilled",
            showOptions=True
        )