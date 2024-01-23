from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

event = {'usuario': 'user1', 'categoria': 'artists', 'lista': ['Aventura', 'Drake', 'Don Omar', 'Rammstein', 'Rauw Alejandro', 'Los 4', 'Slipknot', 'Rihanna', 'Bad Bunny', 'Wisin & Yandel']}

#Providence Sans Bold

now = datetime.now()
caracteres_soportados = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ&')

# Ruta a la imagen de la plantilla
image_path = './POLLADA.png'
# Cargar la imagen
image = Image.open(image_path)

# Preparar el objeto para dibujar
draw = ImageDraw.Draw(image)

# Rutas a las fuentes
font_path = 'd:/MILUNADEV/POLLADAFY/pruebas/font5.otf'
backup_font_path = 'arial.ttf'  # Fuente de respaldo

# Tamaños de fuente
font_size = 80
fontmain_size = 80

# Cargar fuentes
fontmain = ImageFont.truetype(font_path, fontmain_size)
font = ImageFont.truetype(font_path, font_size)
backup_font_datos = ImageFont.truetype(backup_font_path, 50)
backup_font = ImageFont.truetype(backup_font_path, font_size)  # Fuente de respaldo para caracteres especiales


def draw_text(draw, text, position, font, backup_font, fill='black',main=False):
    x, y = position
    for char in text:
        used_font = font if char in caracteres_soportados else backup_font
        draw.text((x, y), char, font=used_font, fill=fill)
        if main==True:
            x += 50
        elif main=='datos':
            x += 30
        else:
            x += 40
    return (x, y)

x,y=1000,420
draw_text(draw, event['usuario'], (x, y), font, backup_font)

x,y=200,710
draw_text(draw, str(now.day) +' ' +str(now.month) +'   24' , (x, y), fontmain, backup_font_datos, main='datos')
x,y=700,710
draw_text(draw, '02:45' , (x, y), fontmain, backup_font_datos, main='datos')
x,y=1150,670
draw_text(draw, 'Huaralino de Comas ' , (x, y), font, backup_font)



# Dibujar el primer artista con la fuente principal
x, y = 1100, 1000
draw_text(draw, event['lista'][0], (x, y), fontmain, backup_font,main=True)

# Función para dibujar grupos de artistas
def draw_artist_group(start_position, artists, line_height):
    x, y = start_position
    for artist in artists:
        draw_text(draw, artist, (x, y), font, backup_font)
        y += line_height

# Dibujar los artistas en grupos de tres con sus posiciones iniciales
positions = [(500, 1200), (1000, 1200), (1700, 1200)]
line_height = font_size + 10

for i, group_start in enumerate(range(1, len(event['lista']) - 1, 3)):
    draw_artist_group(positions[i], event['lista'][group_start:group_start + 3], line_height)

# Guardar la imagen modificada
output_path = 'pollada_filled.png'
image.save('pollada_filled.png')
print("La imagen ha sido guardada como 'pollada_filled.png'")
