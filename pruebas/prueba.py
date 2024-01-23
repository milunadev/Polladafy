from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

event = {
    'usuario': 'user1', 
    'categoria': 'artists', 
    'lista': ['Aventura', 'Drake', 'Don Omar', 'Rammstein', 'Rauw Alejandro', 'Los 4', 'Slipknot', 'Rihanna', 'Bad Bunny', 'Wisin & Yandel']
}

now = datetime.now()

# Ruta a la imagen de la plantilla
image_path = './POLLADA.png'
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Rutas y tamaños de las fuentes
font_path = 'd:/MILUNADEV/POLLADAFY/pruebas/font5.otf'
backup_font_path = 'arial.ttf'  
font_size = 70
fontmain_size = 120
font_date =60
main_font = ImageFont.truetype(font_path, fontmain_size)
font = ImageFont.truetype(font_path, font_size)
date_font = ImageFont.truetype(font_path, font_date)
backup_font = ImageFont.truetype(backup_font_path, font_size)

# Función para dibujar texto completo
def draw_text(draw, text, position, font, fill='black'):
    draw.text(position, text, font=font, fill=fill)

# Dibujar el nombre del usuario y otros datos
draw_text(draw, event['usuario'], (1000, 420), font)
draw_text(draw, f"{now.day} {now.month}    24", (200, 710), date_font)
draw_text(draw, "02:45", (700, 710), date_font)
draw_text(draw, "Huaralino de Comas", (1150, 690), font)

# Dibujar el primer artista
draw_text(draw, event['lista'][0], (1100, 1000), main_font)

# Dibujar los demás artistas
positions = [(450, 1200), (1000, 1200), (1700, 1200)]
line_height = font_size + 10
for i, group_start in enumerate(range(1, len(event['lista']), 3)):
    x, y = positions[i]
    for artist in event['lista'][group_start:group_start + 3]:
       draw_text(draw, artist, (x, y), font)
       y += line_height

output_path = 'pollada_filled.png'
image.save(output_path)
print(f"La imagen ha sido guardada como '{output_path}'")