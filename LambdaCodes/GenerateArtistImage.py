import json
import boto3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from datetime import datetime

# Inicializar cliente S3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    now = datetime.now()
    categoria = event['categoria']
    periodo = event['periodo']
    img_url = event['img']
    print(event)

    # Obtener la imagen de fondo desde S3
    bucket = 'polladafybucket'
    key = 'POLLADA.png'
    obj = s3.get_object(Bucket=bucket, Key=key)
    print('Imagen obtenida de S3, leyendo...')
    image = Image.open(BytesIO(obj['Body'].read()))
    # Preparar el objeto para dibujar
    draw = ImageDraw.Draw(image)

    # Rutas a las fuentes
    font_path = 'font6.ttf'
    font_size = 70
    fontmain_size = 120
    font_date =60
    main_font = ImageFont.truetype(font_path, fontmain_size)
    font = ImageFont.truetype(font_path, font_size)
    date_font = ImageFont.truetype(font_path, font_date)
    # Función para dibujar texto completo
    def draw_text(draw, text, position, font, fill='black'):
        draw.text(position, text, font=font, fill=fill)
    print('DIBUJANDO')
    # Dibujar el nombre del usuario y otros datos
    draw_text(draw, event['usuario'], (850, 350), main_font)
    draw_text(draw, f"{now.day} {now.month}     24", (220, 690), date_font)
    draw_text(draw, "02:45", (700, 690), date_font)
    draw_text(draw, "Huaralino de Comas", (1150, 680), font)

    # Dibujar el primer artista
    draw_text(draw, event['lista'][0], (1100, 1000), main_font)

    # Dibujar los demás artistas
    positions = [(470, 1200), (1000, 1200), (1700, 1200)]
    line_height = font_size + 10
    for i, group_start in enumerate(range(1, len(event['lista']), 3)):
        x, y = positions[i]
        for artist in event['lista'][group_start:group_start + 3]:
            draw_text(draw, artist, (x, y), font)
            y += line_height
    
    #dibujar imagen pequena
    respuesta = requests.get(img_url)
    imagen_pequena = Image.open(BytesIO(respuesta.content)).convert("RGBA")  
    posicion = (1700, 100)    
    image.paste(imagen_pequena, posicion, imagen_pequena)


    # Guardar la imagen modificada en /tmp
    temp_path = '/tmp/pollada_filled.png'
    image.save(temp_path)
    
    # Opcionalmente, subir la imagen modificada de vuelta a S3
    new_key = f"{event['usuario']}/img_{periodo}_{categoria}_filled.png"
    s3.upload_file(temp_path, bucket, new_key)
    print('Imagen subida a S3')
    # Devolver la ruta de la imagen modificada o la URL de S3
    return {
        'statusCode': 200,
        'body': {
        'message': 'Imagen modificada guardada exitosamente',
        's3_key': new_key
        }
    }
       
