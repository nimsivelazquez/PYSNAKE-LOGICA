import pygame

# Inicializar Pygame y el mezclador de audio
pygame.init()
pygame.mixer.init()

# Configuración de la ventana (1280x720)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pysnake - Lógica")
clock = pygame.time.Clock()

# Cargar la música de fondo (puedes cambiar "pysnake_rising.mp3" por el nombre exacto de tu archivo de audio)
try:
  pygame.mixer.music.load("Media/pysnake_rising.mp3")
  pygame.mixer.music.play(-1)  # -1 para que la música se repita en bucle
  print("Música cargada correctamente.")
except Exception as e:
  print(f"No se pudo cargar el archivo de música: {e}")

# Cargar y redimensionar las 3 imágenes de la carpeta Media
imagenes = [
    pygame.transform.scale(
        pygame.image.load("Media/PYSNAKE1.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    ),
    pygame.transform.scale(
        pygame.image.load("Media/PYSNAKE2.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    ),
    pygame.transform.scale(
        pygame.image.load("Media/PYSNAKE3.jpeg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
    ),
]

indice_imagen = 0
tiempo_cambio = 3000  # Cambiar de imagen cada 3000 milisegundos (3 segundos)
ultimo_cambio = pygame.time.get_ticks()

# Bucle principal del juego
running = True
while running:
  # Manejo de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Lógica del temporizador para cambiar la imagen automáticamente
  tiempo_actual = pygame.time.get_ticks()
  if tiempo_actual - ultimo_cambio > tiempo_cambio:
    indice_imagen = (indice_imagen + 1) % len(imagenes)
    ultimo_cambio = tiempo_actual

  # Renderizar en pantalla la imagen actual
  screen.blit(imagenes[indice_imagen], (0, 0))

  # Actualizar la pantalla
  pygame.display.flip()

  # Limitar a 60 cuadros por segundo
  clock.tick(60)

pygame.quit()