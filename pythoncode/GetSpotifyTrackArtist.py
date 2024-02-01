import json
import requests
import boto3
from botocore.exceptions import ClientError

#Inicializamos DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PolladafyDB')
lambdaclient = boto3.client('lambda')
s3 = boto3.client('s3')

def consulta_spotify(access_token,categoria,periodo):
        #SOLICITUD A SPOTIFY TOP
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        # Construir URL de la API
        spotify_url = f'https://api.spotify.com/v1/me/top/{categoria}?time_range={periodo}&limit=10'
        print(spotify_url)
        try:
            spotify_response = requests.get(spotify_url, headers=headers)
            spotify_response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
            spotify_data = spotify_response.json()
            print(spotify_data)
            return spotify_data
            
        except requests.exceptions.RequestException as e:
            print(e)
            # Atrapar cualquier error de la solicitud y devolver un mensaje apropiado
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'ERROR AL CONSULTAR SPOTIFY', 'details': str(e)}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }

def formato_datos(spotify_data, categoria, username, periodo):
    if categoria == 'artists':
        img_url = spotify_data['items'][0]['images'][1]['url']
    else:
        img_url = spotify_data['items'][0]['album']['images'][1]['url']
    print(img_url)
    lista_send = [item['name'] for item in spotify_data['items']]
    data_invocacion = {
        'usuario': username,
        'categoria': categoria,
        'periodo': periodo,
        'lista': lista_send,
        'img': img_url,
    }
    return data_invocacion

def invocar_lambda_generacion_imagen(data_invocacion, lambda_function_name):
    try:
        response = lambdaclient.invoke(
            FunctionName=lambda_function_name,
            InvocationType='RequestResponse', 
            Payload=json.dumps(data_invocacion)
        )
        # Leer el contenido del StreamingBody y convertirlo a una cadena de texto
        response_payload = response['Payload'].read()
        return json.loads(response_payload)  # Convertir la cadena a JSON
    except Exception as e:
        raise RuntimeError(f"Error al invocar Lambda: {str(e)}")

def lambda_handler(event, context):
     # Recuperar parámetros de la consulta
    queryStringParameters = event['queryStringParameters']
    categoria = queryStringParameters['categoria']
    periodo  = queryStringParameters['periodo']
    username = event['headers']['username']
    
    # Recuperar el session token del encabezado
    session_token = event['headers']['session-token']
    print(categoria, periodo)
    
    
    bucket = 'polladafybucket'
    s3_key = f"{username}/img_{periodo}_{categoria}_filled.png"
    
    try:
        # Intenta obtener el objeto de S3
        obj = s3.get_object(Bucket=bucket, Key=s3_key)
        response_dict = {
            'statusCode': 200,
            'body': {
                'message': 'Imagen recuperada del bucket',
                's3_key': s3_key  # `s3_key` debe ser una cadena
            }
        }
        response_body = json.dumps(response_dict['body'])
        return {
            'statusCode': 200,
            'body': response_body,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except ClientError as e:
        #EVALUAMOS SI EL OBJETO YA EXISTE EN EL BUCKET
        if e.response['Error']['Code'] == 'NoSuchKey':
            # El objeto no existe, ejecutar otras funciones.
            response = table.get_item(Key={'session_token': session_token})
            if 'Item' not in response:
                return {'statusCode': 404, 'body': json.dumps({'error': 'Session token not found'})}
            
            access_token = response['Item']['access_token']
            spotify_data = consulta_spotify(access_token, categoria, periodo)
            data_invocacion=formato_datos(spotify_data,categoria,username, periodo)
            
            lambda_function_name = (
                'arn:aws:lambda:us-east-2:208371820303:function:GenerateArtistImage'
                if categoria == 'artists' else
                'arn:aws:lambda:us-east-2:208371820303:function:GenereteTracksImage'
            )
            print('Invocando Lambda ...')
            response_dict = invocar_lambda_generacion_imagen(data_invocacion, lambda_function_name)
            print(response_dict)
            
            return {
                'statusCode': 200,
                'body': json.dumps(response_dict),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        else:
            # Si el error es por otra razón, lanza la excepción
            raise RuntimeError(f"Error de S3: {e.response['Error']['Code']}")