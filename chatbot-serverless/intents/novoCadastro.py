from services.dynamo.user import search_by_phone, insert_user
from utils.lex_utils import generate_lex_response

def novoCadastro(sessionState, sessionAttributes, slots, intentName):
    name = slots.get('nome', {}).get('value', {}).get('interpretedValue', "Não informado")
    email = slots.get('e-mail', {}).get('value', {}).get('interpretedValue', "Não informado")
    phone = slots.get('telefone', {}).get('value', {}).get('interpretedValue', "Não informado")
    age = slots.get('idade', {}).get('value', {}).get('interpretedValue', "Não informado")

    # verify if the phone number is already registered
    result = search_by_phone(phone)

    if not result:
        user = insert_user(name, email, phone, age)  # insert the new user in the database
        print(user)
        sessionAttributes['nome'] = name
        sessionAttributes['e-mail'] = email
        sessionAttributes['telefone'] = phone
        sessionAttributes['idade'] = age
        sessionAttributes['userId'] = user.get('id')

        response_message = "Novo cadastro realizado com sucesso."
    else:
        response_message = "O telefone já está cadastrado."

    return generate_lex_response(
            intentName=intentName,
            sessionState=sessionState,
            sessionAttributes=sessionAttributes,
            message=response_message,
            state="Fulfilled",
            showOptions=True
        )