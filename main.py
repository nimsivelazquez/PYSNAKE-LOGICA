import pygame

# Inicializar Pygame y el mezclador de audio
pygame.init()
pygame.mixer.init()

# Configuración de la ventana (1280x720)
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pysnake - Lógica")
clock = pygame.time.Clock()
musica_cargada = False

# Cargar la música de fondo
try:
  pygame.mixer.music.load("Media/mikesonido.mp3")
  pygame.mixer.music.play(-1)  # -1 para que la música se repita en bucle
  musica_cargada = True
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

# CONFIGURACIÓN DEL BOTÓN MUTE
BOTON_TAM = 50
boton_mute = pygame.Rect(10, 10, BOTON_TAM, BOTON_TAM)
musica_activa = True


def dibujar_boton_mute(surf, rect, activo, hover):
  """Dibuja un pequeño botón con icono de altavoz / mute."""
  color_fondo = (70, 70, 70) if hover else (30, 30, 30)
  pygame.draw.rect(surf, color_fondo, rect, border_radius=10)
  pygame.draw.rect(surf, (220, 220, 220), rect, 2, border_radius=10)

  cx, cy = rect.center
  s = rect.width // 2  # escala

  color = (255, 255, 255) if activo else (170, 170, 170)

  # Base del altavoz
  pygame.draw.rect(surf, color, (cx - s * 0.6, cy - s * 0.25, s * 0.35, s * 0.5))
  # Cono del altavoz
  pygame.draw.polygon(surf, color, [
      (cx - s * 0.3, cy - s * 0.5),
      (cx - s * 0.3, cy + s * 0.5),
      (cx + s * 0.15, cy + s * 0.75),
      (cx + s * 0.15, cy - s * 0.75),
  ])

  if activo:
    # Ondas de sonido
    for r in (s * 0.55, s * 0.85):
      pygame.draw.arc(
          surf, color, (cx + s * 0.05 - r, cy - r, r * 2, r * 2), -0.9, 0.9, 2
      )
  else:
    # Cruz roja de mute
    pygame.draw.line(
        surf, (255, 60, 60), (cx + s * 0.1, cy - s * 0.6), (cx + s * 0.9, cy + s * 0.6), 3
    )
    pygame.draw.line(
        surf, (255, 60, 60), (cx + s * 0.9, cy - s * 0.6), (cx + s * 0.1, cy + s * 0.6), 3
    )


# Bucle principal del juego
running = True
while running:
  # Manejo de eventos
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    # Clic sobre el botón de mute (CORREGIDO)
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
      if boton_mute.collidepoint(event.pos) and musica_cargada:
        if musica_activa:
          pygame.mixer.music.pause()
          musica_activa = False
        else:
          pygame.mixer.music.unpause()
          musica_activa = True

  # Lógica del temporizador para cambiar la imagen automáticamente
  tiempo_actual = pygame.time.get_ticks()
  if tiempo_actual - ultimo_cambio > tiempo_cambio:
    indice_imagen = (indice_imagen + 1) % len(imagenes)
    ultimo_cambio = tiempo_actual

  # Renderizar en pantalla la imagen actual
  screen.blit(imagenes[indice_imagen], (0, 0))

  # Render del botón de mute (encima de la imagen)
  hover = boton_mute.collidepoint(pygame.mouse.get_pos())
  dibujar_boton_mute(screen, boton_mute, musica_activa, hover)

  # Actualizar la pantalla
  pygame.display.flip()
  clock.tick(60)

pygame.quit()