from services.dynamo_service import get_pets, get_pet_by_name_and_breed

def generate_lex_response(intentName, sessionState, sessionAttributes, message, state="Fulfilled", showOptions=False):
    # Atualiza sessionState com sessionAttributes
    sessionState['sessionAttributes'] = sessionAttributes
    sessionState['dialogAction'] = {
        "type": "Close",
    }
    sessionState['intent'] = {
        "name": intentName,
        "state": state
    }

    messages = [
        {
        "contentType": "PlainText",
        "content": message
        }
    ]

    if showOptions and sessionAttributes.get('nome'):
        MENU_STRING = (f"O que você deseja fazer agora {sessionAttributes['nome']}? \n \n"
                        "1. Adotar um Animal \n"
                        "2. Realizar doação para ONG \n"
                        "3. Dicas de Cuidado com meu animal \n")


        messages.append({
            "contentType": "CustomPayload",
            "content": MENU_STRING
        })
    
    lex_response_json = {
        "sessionState": sessionState,
        "messages": messages
    }

    return lex_response_json
    

def animal_exists(animal_name):
    """
    Verifica se o animal especificado existe no banco de dados.
    """
    name, breed = animal_name.split(" - ")
    pet = get_pet_by_name_and_breed(name, breed)
    print(pet)
    if pet:
        return pet

    return False