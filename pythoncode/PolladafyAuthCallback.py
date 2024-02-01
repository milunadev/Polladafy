import json
import requests
import boto3
import uuid

#Inicializamos DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PolladafyDB')

def request_user(access_token):
    headers = {
            'Authorization': f'Bearer {access_token}'
    }
    spotify_url = 'https://api.spotify.com/v1/me'
    try:
        spotify_response = requests.get(spotify_url, headers=headers)
        spotify_response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        spotify_data = spotify_response.json()
        return spotify_data['display_name']
    except:
        return 'Error getting user'

def lambda_handler(event, context):
    code = event.get('queryStringParameters', {}).get('code')
    if code:
        redirect_uri = 'https://fh8qwcz15a.execute-api.us-east-2.amazonaws.com/auth/spotify/callback'
        client_id = ''  # Asegúrate de que esto es correcto
        client_secret = ''  # Asegúrate de que esto es correcto
        
        try:
            # Realiza la solicitud a Spotify para obtener los tokens
            response = requests.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'client_id': client_id,
                    'client_secret': client_secret
                }
            )
            
            # Verifica si la respuesta es exitosa
            if response.status_code == 200:
                tokens = response.json()
                print(tokens)
                print("Token de acceso obtenido de Spotify: ", tokens['access_token'])
                session_token = str(uuid.uuid4())
                user_response = request_user(tokens['access_token'])
                try:
                    response = table.put_item(
                    Item={
                        'session_token': session_token,
                        'access_token': tokens['access_token'],
                        'refresh_token': tokens['refresh_token'],
                        'username': user_response,
                        # Puedes guardar también otros datos como 'expires_in', 'scope', etc.
                        }
                    )
                # Manejo de la respuesta de DynamoDB si es necesario...
                except Exception as e:
                    print(e)
                    return {
                            'statusCode': 500,
                            'body': 'Error al guardar los tokens en DynamoDB'
                    }
                return {
                    'statusCode': 302,
                    'headers': {
                        'Location': f'http://localhost:3000/dashboard?session_token={session_token}&username={user_response}'
                    }
                }
            else:
                print(response)
                return {
                    'statusCode': response.status_code,
                    'body': "Error al obtener tokens de Spotify"
                }
    
        except Exception as e:
            print(e)
            return {
                'statusCode': 500,
                'body': 'Error interno del servidor'
            }
    else:
        print("Se cancelo desde login Spotify")
        return {
            'statusCode': 302,
            'headers': {
                        'Location': f'http://localhost:3000'
            }
        }