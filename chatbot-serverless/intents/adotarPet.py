from services.dynamo.pets import get_pets
from services.dynamo.adopt_solicitations import insert_adopt_solicitation
from utils.lex_utils import animal_exists

def adotarPet(event):
    intent_name = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    slot_name = "AnimalToAdopt"
    sessionAttributes = event['sessionState'].get('sessionAttributes', {})

    if intent_name == "adotarPet":
        # verify if the user has chosen an animal
        if slots.get(slot_name) and slots[slot_name].get('value'):
            animal_chosen = slots[slot_name]['value']['interpretedValue']
            # validate if the animal exists in the database
            pet = animal_exists(animal_chosen)
            print("Pet na intent adotarPet", pet) 
            if pet:
                print(sessionAttributes)
                pet_id = pet.get('id')
                user_id = sessionAttributes.get('userId')
                phone = sessionAttributes.get('phone')

                if insert_adopt_solicitation(pet_id, phone, user_id) is None:
                    return close_dialog(
                        sessionAttributes,
                        intent_name,
                        "Desculpe, ocorreu um erro ao tentar adotar o animal. Por favor, tente novamente.",
                        slots
                    )
                else:
                    return close_dialog(
                        sessionAttributes,
                        intent_name,
                        f"Sua solicitação para adotar o animal {pet['nome']} foi recebida. Em breve entraremos em contato.",
                        slots
                    )
            else:
                # return a message if the animal chosen is not available
                return elicit_slot_with_list(
                    session_attributes=sessionAttributes,
                    intent_name=intent_name,
                    slot_to_elicit=slot_name,
                    message="O animal escolhido não está disponível. Por favor, escolha da lista abaixo:",
                    options=show_pets_list()
                )

        # search for available pets in the database
        animal_options = show_pets_list()

        # return a message if there are no animals available
        if not animal_options:
            return close_dialog(
                intent_name,
                "Desculpe, não temos animais disponíveis no momento.",
                slots
            )

        # return the list of available pets to the user
        return elicit_slot_with_list(
            session_attributes=sessionAttributes,
            intent_name=intent_name,
            slot_to_elicit=slot_name,
            message="Aqui estão os animais disponíveis para adoção. Qual você prefere? Digite a resposta no seguinte formato (Nome - Raça)",
            options=animal_options
        )


def show_pets_list():
    """
    Builds and returns a list of animals available for adoption.

    Returns:
        list: A list of strings with information about available pets, or an empty list if no pets are available.
    """
    pets = get_pets()
    
    # Ensure `pets` is a valid list
    if not pets or not isinstance(pets, list):
        return []

    # Format the results, filtering only available pets
    formatted_pets = [
        f"{pet.get('nome', 'Unknown')} - {pet.get('especie', 'Unknown')} - {pet.get('raça', 'Unknown')}"
        for pet in pets if pet.get('disponivel', True)
    ]

    return formatted_pets



def elicit_slot_with_list(session_attributes, intent_name, slot_to_elicit, message, options):
    """
    Monta a resposta do Lex com uma lista de opções no payload.
    """

    options_string = "\n".join(options)

    return {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitSlot",
                "slotToElicit": slot_to_elicit
            },
            "intent": {
                "name": intent_name,
                "slots": {}
            },
            "sessionAttributes": session_attributes
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            },
            {
                "contentType": "CustomPayload",
                "content": options_string
            }
        ],
    }

def close_dialog(session_attributes, intentName, message, slots):
    """
    Fecha o diálogo quando a interação é concluída.
    """
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": intentName,
                "state": "Fulfilled",
                "slots": slots
            },
            "sessionAttributes": session_attributes
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }