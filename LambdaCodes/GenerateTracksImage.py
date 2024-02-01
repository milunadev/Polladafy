import json
import boto3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
from datetime import datetime

# Inicializar cliente S3
s3 = boto3.client('s3')

def lambda_handler(event, context):
    img_url = event['img']
    now = datetime.now()
    categoria = event['categoria']
    periodo = event['periodo']
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
    font_size = 60
    fontmain_size = 100
    font_date = 60
    main_font = ImageFont.truetype(font_path, fontmain_size)
    font = ImageFont.truetype(font_path, font_size)
    date_font = ImageFont.truetype(font_path, font_date)
    

    # Función para dibujar texto completo
    def draw_text(draw, text, position, font, fill=(54, 55, 94)):
        draw.text(position, text, font=font, fill=fill)

    # Dibujar el nombre del usuario y otros datos
    draw_text(draw, event['usuario'], (1000, 400), main_font)
    draw_text(draw, f"{now.day} {now.month}     24", (220, 690), date_font)
    draw_text(draw, "02:45", (700, 690), date_font)
    draw_text(draw, "Huaralino de Comas", (1150, 690), font)

    # Dibujar el primer artista
    draw_text(draw, event['lista'][0], (1000, 980), main_font)
    
    print("Dibujadas las primeras lineas")

    max_width_column = 700  # Ajusta según la necesidad
    column_positions = [(500, 1130), (1450, 1130)]  # Ajusta según la necesidad
    column_y = [1200, 1200]  # Posiciones iniciales de y para cada columna
    x1, y1 = column_positions[0]
    x2, y2 = column_positions[1]
    

    def divide_texto(y1,x1,texto, font, draw,max_width_column = 650):
        palabras = texto.split()
        lineas = []
        linea_actual = ''
        for palabra in palabras:
            prueba_linea = f'{linea_actual} {palabra}'.strip()
            ancho_linea = draw.textlength(prueba_linea, font=font)
            if ancho_linea <= max_width_column:
                # Si no excede, sigue construyendo la línea actual
                linea_actual = prueba_linea
            else:
                # Si excede, guarda la línea actual y comienza una nueva
                draw.textlength(linea_actual, font=font)
                lineas.append(linea_actual)
                linea_actual = palabra
                
        if linea_actual:
            lineas.append(linea_actual)
        draw_text(draw, '- '+lineas[0], (x1, y1), font)
        y1+=font_size
        draw_text(draw, lineas[1], (x1, y1), font)
        y1+=font_size+10
        return y1     
        
    print("Dibujando canciones")

    for i, artist in enumerate(event['lista'][1:6]):
        lenght = draw.textlength(artist, font=font)
        if lenght > 700:
            ya = divide_texto(y1,x1,artist,font=font,draw=draw)
            y1 = ya
        else:
            
            draw_text(draw, '- '+artist, (x1, y1), font)
            y1+=font_size+10

    for i, artist in enumerate(event['lista'][6:11]):
        lenght = draw.textlength(artist, font=font)
        if lenght > 700:
            ya = divide_texto(y2,x2,artist,font=font,draw=draw)
            y2 = ya
        else:
            draw_text(draw, '- '+artist, (x2, y2), font)
            y2+=font_size+10
            
    #dibujar imagen pequena
    respuesta = requests.get(img_url)
    imagen_pequena = Image.open(BytesIO(respuesta.content)).convert("RGBA")  
    posicion = (1700, 100)    
    image.paste(imagen_pequena, posicion, imagen_pequena)
     
    print("Dibujo terminado")
    
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
       
