#Importo la librería 'sys' para poder cerrar el programa de forma segura desde la consola.
import sys

#Importo 'random' para que la comida aparezca en posiciones aleatorias dentro de la pantalla.
import random

#Importo 'winsound' para emitir un pitido de sonido nativo en Windows cada vez que la serpiente coma.
import winsound

#Importo la librería principal 'pygame' para desarrollar la interfaz y la lógica del videojuego.
import pygame

#Inicializo todos los módulos internos necesarios de Pygame para que funcionen sin problemas.
pygame.init()

#Inicializo específicamente el subsistema de audio de Pygame para garantizar estabilidad con el sonido.
pygame.mixer.init()

#---------------------------------------------------------
#CONFIGURACIÓN DE CONSTANTES Y DIMENSIONES
#---------------------------------------------------------
ANCHO = 600  #Ancho total de la ventana del juego en píxeles.
ALTO = 400   #Alto total de la ventana del juego en píxeles.
TAMANO_BLOQUE = (
    20  #Tamaño en píxeles de cada cuadrito de la serpiente y de la comida.
)
VELOCIDAD_JUEGO = (
    10  #Controla los fotogramas por segundo (FPS), regulando qué tan rápido se mueve.
)

#Defino una paleta de colores personalizada en formato RGB (Rojo, Verde, Azul) para una estética limpia.
COLOR_FONDO = (245, 243, 239)  #Color crema suave para el fondo.
COLOR_TEXTO = (47, 60, 126)    #Color azul oscuro para los textos y puntuaciones.
COLOR_SERPIENTE = (
    111,
    150,
    114,
)  #Color verde pastel para el cuerpo de la serpiente.
COLOR_CABEZA = (
    73,
    107,
    76,
)  #Color verde un poco más oscuro para diferenciar la cabeza.
COLOR_COMIDA = (219, 112, 112)  #Color coral suave para el bloque de comida.
COLOR_GRID = (
    230,
    225,
    215,
)  #Color sutil para la cuadrícula de referencia en el fondo.

#Creo la ventana gráfica principal del juego utilizando el ancho y alto definidos.
pantalla = pygame.display.set_mode((ANCHO, ALTO))

#Asigno un título oficial que aparecerá en la barra superior de la ventana.
pygame.display.set_caption("Snake Microproject - Desarrollo Individual")

#Inicializo el reloj del sistema para controlar los tiempos y la velocidad de actualización de la pantalla.
reloj = pygame.time.Clock()

#Cargo las fuentes tipográficas estilo Arial en diferentes tamaños (con negrita activada) para los textos.
fuente_std = pygame.font.SysFont("Arial", 22, bold=True)
fuente_tit = pygame.font.SysFont("Arial", 36, bold=True)


#-------------------------------
#FUNCIONES DE APOYO Y MENÚS
#-------------------------------
def dibujar_cuadricula():
  """Dibuja una cuadrícula de referencia estética en el fondo de la pantalla."""
  #Dibujo líneas verticales a lo largo de todo el ancho según el tamaño del bloque.
  for x in range(0, ANCHO, TAMANO_BLOQUE):
    pygame.draw.line(pantalla, COLOR_GRID, (x, 0), (x, ALTO))
  #Dibujo líneas horizontales a lo largo de todo el alto según el tamaño del bloque.
  for y in range(0, ALTO, TAMANO_BLOQUE):
    pygame.draw.line(pantalla, COLOR_GRID, (0, y), (ANCHO, y))


def mostrar_menu_inicio():
  """Muestra la interfaz del menú principal antes de iniciar la partida."""
  en_menu = True
  while en_menu:
    #Relleno toda la pantalla con el color de fondo base.
    pantalla.fill(COLOR_FONDO)

    #Renderizo en memoria los textos principales del título y las instrucciones de control.
    titulo = fuente_tit.render("SNAKE MICROPROJECT", True, COLOR_TEXTO)
    subtitulo = fuente_std.render(
        "Presiona [ESPACIO] para Iniciar o [ESC] para Salir", True, COLOR_SERPIENTE
    )

    #Dibujo y centro el título y subtítulo en la pantalla de forma automática.
    pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, ALTO // 3))
    pantalla.blit(
        subtitulo, (ANCHO // 2 - subtitulo.get_width() // 2, ALTO // 2 + 10)
    )

    #Actualizo los gráficos en pantalla usando doble buffering.
    pygame.display.flip()

    #Reviso la cola de eventos del sistema operativo para capturar las acciones del usuario.
    for evento in pygame.event.get():
      #Si el usuario hace clic en la 'X' de la ventana, cierro el programa por completo.
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      #Si el usuario presiona una tecla del teclado:
      if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_SPACE:
          en_menu = False  #Rompo el ciclo del menú y arranco el juego al presionar Espacio.
        elif evento.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()  # Cierro el programa si presiona la tecla Escape.
    #Limito los fotogramas del menú a 15 FPS para no consumir recursos innecesarios.
    reloj.tick(15)


#---------------------------------------------
#BUCLE PRINCIPAL DEL JUEGO (GAME LOOP)
#---------------------------------------------
def bucle_juego():
  """Gestiona la lógica principal, movimiento, colisiones, input y sonido."""
  #Defino las coordenadas iniciales de la serpiente como una lista de segmentos (cabeza y cuerpo).
  snake = [[100, 100], [80, 100], [60, 100]]
  direccion = "DERECHA"  #Establezco la dirección inicial de movimiento hacia la derecha.
  siguiente_dir = direccion

  #Genero la posición inicial de la comida de forma aleatoria y alineada a la cuadrícula.
  comida = [
      random.randrange(0, ANCHO // TAMANO_BLOQUE) * TAMANO_BLOQUE,
      random.randrange(0, ALTO // TAMANO_BLOQUE) * TAMANO_BLOQUE,
  ]

  puntuacion = 0  #Inicializo el contador de puntos en cero.
  jugando = True  #Bandera principal que mantiene el juego activo mientras no pierda.

  while jugando:
    #1. MANEJO DE INPUT (Eventos de Teclado)
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      elif evento.type == pygame.KEYDOWN:
        #Verifico las teclas de dirección evitando giros de 180 grados instantáneos sobre sí misma.
        if evento.key == pygame.K_UP and direccion != "ABAJO":
          siguiente_dir = "ARRIBA"
        elif evento.key == pygame.K_DOWN and direccion != "ARRIBA":
          siguiente_dir = "ABAJO"
        elif evento.key == pygame.K_LEFT and direccion != "DERECHA":
          siguiente_dir = "IZQUIERDA"
        elif evento.key == pygame.K_RIGHT and direccion != "IZQUIERDA":
          siguiente_dir = "DERECHA"

    #Actualizo la dirección definitiva con la tecla seleccionada.
    direccion = siguiente_dir

    #2. ACTUALIZACIÓN DE LA POSICIÓN (Lógica de Movimiento)
    cabeza_x, cabeza_y = snake[0]  #Tomo las coordenadas actuales de la cabeza.
    #Modifico la posición de la cabeza sumando o restando el tamaño del bloque según la dirección.
    if direccion == "ARRIBA":
      cabeza_y -= TAMANO_BLOQUE
    elif direccion == "ABAJO":
      cabeza_y += TAMANO_BLOQUE
    elif direccion == "IZQUIERDA":
      cabeza_x -= TAMANO_BLOQUE
    elif direccion == "DERECHA":
      cabeza_x += TAMANO_BLOQUE

    #Creo la nueva posición de la cabeza con las coordenadas actualizadas.
    nueva_cabeza = [cabeza_x, cabeza_y]

    #Validaciones de fin de juego: compruebo si choca contra los bordes de la ventana.
    if not (0 <= cabeza_x < ANCHO and 0 <= cabeza_y < ALTO):
      jugando = False
    #Compruebo si la cabeza colisiona con cualquier parte de su propio cuerpo.
    if nueva_cabeza in snake:
      jugando = False

    #Inserto la nueva cabeza al inicio de la lista que compone la serpiente.
    snake.insert(0, nueva_cabeza)

    #Verifico si la serpiente colisiona exactamente en el mismo espacio donde está la comida.
    if nueva_cabeza == comida:
      puntuacion += 10  #Incremento 10 puntos al marcador.
      #Reproduzco un pitido de audio automático utilizando winsound (Frecuencia 800Hz, Duración 100ms).
      try:
        winsound.Beep(800, 100)
      except Exception:
        pass

      #Reubico la comida en una nueva posición aleatoria dentro de la cuadrícula.
      comida = [
          random.randrange(0, ANCHO // TAMANO_BLOQUE) * TAMANO_BLOQUE,
          random.randrange(0, ALTO // TAMANO_BLOQUE) * TAMANO_BLOQUE,
      ]
    else:
      #Si no comió, remuevo el último segmento de la cola para conservar el tamaño actual.
      snake.pop()

    #3. RENDERIZADO GRÁFICO DE LA ESCENA ACTUAL
    pantalla.fill(COLOR_FONDO)  #Limpio la pantalla rellenándola con el color de fondo.
    dibujar_cuadricula()   #Pinto la cuadrícula de referencia visual.

    #Dibujo el rectángulo correspondiente a la comida en su respectiva posición.
    pygame.draw.rect(
        pantalla,
        COLOR_COMIDA,
        (comida[0], comida[1], TAMANO_BLOQUE, TAMANO_BLOQUE),
        border_radius=4,
    )

    #Recorro con un ciclo cada segmento de la serpiente para dibujarlos uno por uno.
    for idx, segmento in enumerate(snake):
       #Asigno un color diferenciado a la cabeza (índice 0) en comparación con el resto del cuerpo.
      color_bloque = COLOR_CABEZA if idx == 0 else COLOR_SERPIENTE
      pygame.draw.rect(
          pantalla,
          color_bloque,
          (segmento[0], segmento[1], TAMANO_BLOQUE, TAMANO_BLOQUE),
          border_radius=5,
      )

    #Renderizo el texto dinámico que muestra la puntuación actual en la esquina superior izquierda.
    texto_puntuacion = fuente_std.render(
        f"Puntuación: {puntuacion}", True, COLOR_TEXTO
    )
    pantalla.blit(texto_puntuacion, (15, 15))

    #Actualizo toda la pantalla de golpe utilizando doble buffering para evitar parpadeos.
    pygame.display.flip()
    #Limito los fotogramas por segundo según la velocidad configurada del juego.
    reloj.tick(VELOCIDAD_JUEGO)

   #Al terminar el juego, llamo a la pantalla de Game Over pasando la puntuación final obtenida.
  return mostrar_pantalla_game_over(puntuacion)


#---------------------------------------------
#PANTALLA DE FIN DE JUEGO (GAME OVER)
#---------------------------------------------
def mostrar_pantalla_game_over(puntuacion):
  """Muestra la pantalla de Game Over permitiendo reiniciar o salir."""
  esperando = True
  while esperando:
    pantalla.fill(COLOR_FONDO)

    #Renderizo los mensajes de fin de partida, puntaje final y opciones de control.
    t_over = fuente_tit.render("¡FIN DEL JUEGO!", True, COLOR_COMIDA)
    t_score = fuente_std.render(
        f"Puntuación Final: {puntuacion}", True, COLOR_TEXTO
    )
    t_opciones = fuente_std.render(
        "Presiona [R] para Reiniciar o [ESC] para Salir", True, COLOR_SERPIENTE
    )

    #Dibujo y centro cada uno de los textos informativos en pantalla.
    pantalla.blit(t_over, (ANCHO // 2 - t_over.get_width() // 2, ALTO // 3))
    pantalla.blit(t_score, (ANCHO // 2 - t_score.get_width() // 2, ALTO // 2))
    pantalla.blit(
        t_opciones, (ANCHO // 2 - t_opciones.get_width() // 2, ALTO // 2 + 50)
    )

    #Actualizo los gráficos de la pantalla de cierre.
    pygame.display.flip()

    #Escucho los eventos del teclado para saber si el usuario decide reiniciar o salir.
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_r:
          return True  #Retorna True para reiniciar el ciclo principal del juego.
        elif evento.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()  #Cierra la aplicación si presiona Escape.
    reloj.tick(15)

#-----------------------------------------------
#BLOQUE PRINCIPAL DE EJECUCIÓN DEL SCRIPT
#-----------------------------------------------
if __name__ == "__main__":
  #Llamo primero al menú de inicio antes de que comience el bucle de partidas.
  mostrar_menu_inicio()
  #Mantengo un ciclo infinito para permitir reiniciar el juego cuantas veces quiera el usuario.
  while True:
    reiniciar_partida = bucle_juego()
    if not reiniciar_partida:
      break  #Rompe el ciclo y finaliza el programa si el usuario decide no continuar.