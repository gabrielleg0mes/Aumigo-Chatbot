import os
import json
from services.s3_service import get_image

S3_BUCKET = os.getenv('S3_BUCKET_NAME')

def doacaoOng(event):
    intent_name = event['sessionState']['intent']['name']
    sessionAttributes = event['sessionState'].get('sessionAttributes', {})
    pix_image = f'https://{S3_BUCKET}.s3.amazonaws.com/images/Projeto_Compass.png'

    message_formatted = (f"Você pode realizar sua doação para a ONG através do QRCODE de PIX acima! <3 \n"
                        "Agradecemos sua iniciativa para a doação, qualquer valor será bem-vindo! \n\n")

    
    return {
        "sessionState": {
            "sessionAttributes": sessionAttributes,
            "dialogAction": {
                "type": "Close",
            },
            "intent": {
                "name": intent_name,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "CustomPayload",
                "content": message_formatted
            },
            {
                "contentType": "ImageResponseCard",
                    "imageResponseCard": {
                        "title": "Imagem do PIX",
                        "imageUrl": pix_image
                    }
            }
    ]
    }