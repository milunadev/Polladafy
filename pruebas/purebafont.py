#Skippy Sharpie Regular
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

event = {
    'usuario': 'user1', 
    'categoria': 'artists', 
    'lista': ['Empty Walls', 'Reggaetoneando', 'Un Poco Loca (feat. De La Ghetto)', 'Aerials', 'La Ocasión', 'Chop Suey!', 'Escápate Conmigo - Remix', 'Before I Forget', 'LOKERA', 'The Beautiful People']
}

now = datetime.now()

# Ruta a la imagen de la plantilla
image_path = './POLLADA.png'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Rutas y tamaños de las fuentes
font_path = 'd:/MILUNADEV/POLLADAFY/pruebas/font6.ttf'
backup_font_path = 'arial.ttf'  
font_size = 60
fontmain_size = 100
font_date = 60
main_font = ImageFont.truetype(font_path, fontmain_size)
font = ImageFont.truetype(font_path, font_size)
date_font = ImageFont.truetype(font_path, font_date)
backup_font = ImageFont.truetype(backup_font_path, font_size)

# Función para dibujar texto completo
def draw_text(draw, text, position, font, fill=(54, 55, 94)):
    draw.text(position, text, font=font, fill=fill)

# Dibujar el nombre del usuario y otros datos
draw_text(draw, event['usuario'], (1000, 400), main_font)
draw_text(draw, f"{now.day} {now.month}     24", (220, 690), date_font)
draw_text(draw, "02:45", (700, 690), date_font)
draw_text(draw, "Huaralino de Comas", (1150, 690), font)

# Dibujar el primer artista
draw_text(draw, event['lista'][0], (1100, 980), main_font)


max_width_column = 700  # Ajusta según la necesidad
column_positions = [(500, 1130), (1450, 1130)]  # Ajusta según la necesidad
column_y = [1200, 1200]  # Posiciones iniciales de y para cada columna
x1, y1 = column_positions[0]
x2, y2 = column_positions[1]

def divide_texto(y1,x1,texto, font, draw,max_width_column = 650):
    palabras = texto.split()
    lineas = []
    linea_actual = ''
    print('funcion',y1)
    for palabra in palabras:
        prueba_linea = f'{linea_actual} {palabra}'.strip()
        ancho_linea = draw.textlength(prueba_linea, font=font)
        if ancho_linea <= max_width_column:
            # Si no excede, sigue construyendo la línea actual
            linea_actual = prueba_linea
        else:
            print('excede ',linea_actual)
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
    print(lineas)    
    return y1     
    


for i, artist in enumerate(event['lista'][1:6]):
    lenght = draw.textlength(artist, font=font)
    if lenght > 700:
        ya = divide_texto(y1,x1,artist,font=font,draw=draw)
        y1 = ya
    else:
        
        draw_text(draw, '- '+artist, (x1, y1), font)
        y1+=font_size+10
    print(i,artist,x1,y1,lenght)

for i, artist in enumerate(event['lista'][5:10]):
    lenght = draw.textlength(artist, font=font)
    if lenght > 700:
        ya = divide_texto(y2,x2,artist,font=font,draw=draw)
        y2 = ya
    else:
        draw_text(draw, '- '+artist, (x2, y2), font)
        y2+=font_size+10
    print(i,artist,x2,y2,lenght)
    
    
    

output_path = 'pollada_filled6.png'
image.save(output_path)
print(f"La imagen ha sido guardada como '{output_path}'")