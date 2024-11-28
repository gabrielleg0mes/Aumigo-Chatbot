import boto3
import os

S3_BUCKET = os.getenv('S3_BUCKET_NAME')

def get_image(file_name, expiration=3600):
    """
    Generates a pre-signed URL to access an object stored in S3.

    Args:
        file_name (str): The name of the file in the S3 bucket.
        expiration (int): Expiration time for the pre-signed URL in seconds (default: 3600).

    Returns:
        str: The pre-signed URL for the file in S3.
        None: If an error occurs during the URL generation process.
    """
    if not S3_BUCKET:
        print("Erro: O nome do bucket S3 não foi configurado. Verifique a variável de ambiente 'S3_BUCKET_NAME'.")
        return None

    s3 = boto3.client('s3')

    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': S3_BUCKET,
                'Key': file_name
            },
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        print(f"Erro ao gerar URL para o arquivo '{file_name}' no bucket '{S3_BUCKET}': {e}")
        return None
