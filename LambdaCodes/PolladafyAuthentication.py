import json

def lambda_handler(event, context):
    client_id = 'dae7b95560274253bbea3442604a79a8'
    redirect_uri = 'https://fh8qwcz15a.execute-api.us-east-2.amazonaws.com/auth/spotify/callback'
    scope = 'user-top-read user-read-recently-played user-read-private'
    
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}&show_dialog=true"
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'authUrl': auth_url})
    }
