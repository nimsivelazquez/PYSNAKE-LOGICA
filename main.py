import pygame
import random

#Inicializo todos los módulos de Pygame para que la ventana y gráficos arranquen bien
pygame.init()

# Defino mi paleta de colores en formato RGB con tonos modernos y llamativos para el juego
NEGRO = (20, 20, 30)           #Fondo oscuro azulado muy limpio y elegante
VERDE_SNAKE = (46, 204, 113)   #Verde brillante para el cuerpo de la serpiente
CABEZA_SNAKE = (39, 174, 96)   #Un tono de verde un poco más fuerte para distinguir la cabeza
ROJO_MANZANA = (231, 76, 60)   #Rojo vibrante para ubicar fácilmente la manzana
BLANCO = (255, 255, 255)       #Blanco para textos y bordes claros
AZUL_BOTON = (52, 152, 219)    #Color base para mi botón de inicio
AZUL_HOVER = (41, 128, 185)    #Color que toma el botón al pasar el mouse por encima
COLOR_MARCO = (52, 73, 94)     #Color del marco decorativo tipo tablero

#Configuro el tamaño de la ventana de juego y el ancho de cada bloque o celda
ANCHO, ALTO = 600, 400
TAMANO_BLOQUE = 20
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego Snake Didáctico - Microproyecto Pygame")

#Configuro mi reloj para controlar los FPS y asegurar que la serpiente avance a buen ritmo
reloj = pygame.time.Clock()

def generar_comida():
    """Función para crear la comida en coordenadas aleatorias pero exactas dentro de la cuadrícula."""
    col_x = random.randrange(1, (ANCHO // TAMANO_BLOQUE) - 1) * TAMANO_BLOQUE
    col_y = random.randrange(2, (ALTO // TAMANO_BLOQUE) - 1) * TAMANO_BLOQUE
    return [col_x, col_y]

def ejecutar_juego():
    #Cargo las fuentes con estilos llamativos (Arial Black y Verdana) para darle un toque más didáctico
    fuente_titulo = pygame.font.SysFont("Arial Black", 36, bold=True)
    fuente_sub = pygame.font.SysFont("Verdana", 22, bold=True)
    fuente = pygame.font.SysFont("Arial", 18, bold=True)

    #El juego arranca primero mostrando el menú de bienvenida
    estado = "INICIO"
    
    #Posición inicial de mi serpiente (comienza con 3 bloques alineados horizontalmente)
    snake = [[100, 100], [80, 100], [60, 100]]
    direccion = "DERECHA"
    cambio_dir = direccion

    #Coloco la primera manzana en el mapa y pongo mi puntuación en cero
    comida = generar_comida()
    puntuacion = 0

    #Defino las medidas exactas y la posición centrada del botón interactivo del menú
    ancho_btn, alto_btn = 180, 50
    x_btn = (ANCHO - ancho_btn) // 2
    y_btn = 240
    rect_boton = pygame.Rect(x_btn, y_btn, ancho_btn, alto_btn)

    ejecutando = True

    while ejecutando:
        pos_mouse = pygame.mouse.get_pos()

        #==========================================================
        #PANTALLA 1: Menú de inicio interactivo con diseño colorido
        #==========================================================
        if estado == "INICIO":
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                #Si doy clic izquierdo sobre el botón del menú, cambio el estado a "JUGANDO"
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if rect_boton.collidepoint(pos_mouse):
                        estado = "JUGANDO"
                #O si el usuario presiona la tecla Enter en su teclado, también arranca el juego
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        estado = "JUGANDO"

            #Pinto el fondo general de la pantalla
            pantalla.fill(NEGRO)
            
            #Dibujo un marco decorativo para que parezca una pantalla o tablero didáctico
            pygame.draw.rect(pantalla, COLOR_MARCO, (15, 15, ANCHO - 30, ALTO - 30), 3, border_radius=12)

            #Pinto el título principal con un efecto de sombra para que tenga relieve y destaque bonito
            txt_sombra = fuente_titulo.render("¡SUPER SNAKE!", True, (40, 40, 50))
            txt_titulo = fuente_titulo.render("¡SUPER SNAKE!", True, VERDE_SNAKE)
            pantalla.blit(txt_sombra, (ANCHO // 2 - txt_titulo.get_width() // 2 + 2, 92))
            pantalla.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 90))

            #Instrucciones claras en pantalla
            txt_instrucc = fuente.render("Usa las flechas del teclado para moverte", True, BLANCO)
            pantalla.blit(txt_instrucc, (ANCHO // 2 - txt_instrucc.get_width() // 2, 160))

            #Cambio el color del botón si el cursor pasa por encima (efecto hover visual)
            color_btn = AZUL_HOVER if rect_boton.collidepoint(pos_mouse) else AZUL_BOTON
            pygame.draw.rect(pantalla, color_btn, rect_boton, border_radius=12)
            pygame.draw.rect(pantalla, BLANCO, rect_boton, 2, border_radius=12) # Borde blanco decorativo

            #Texto centrado dentro del botón de juego
            txt_boton = fuente_sub.render("JUGAR", True, BLANCO)
            pantalla.blit(txt_boton, (rect_boton.centerx - txt_boton.get_width() // 2, 
                                      rect_boton.centery - txt_boton.get_height() // 2))

            pygame.display.flip()
            reloj.tick(30)

        #==========================================================
        #PANTALLA 2: Lógica principal y desarrollo del juego Snake
        #==========================================================
        elif estado == "JUGANDO":
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                #Leo las teclas de dirección validando que no gire en sentido contrario de golpe
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP and direccion != "ABAJO":
                        cambio_dir = "ARRIBA"
                    elif evento.key == pygame.K_DOWN and direccion != "ARRIBA":
                        cambio_dir = "ABAJO"
                    elif evento.key == pygame.K_LEFT and direccion != "DERECHA":
                        cambio_dir = "IZQUIERDA"
                    elif evento.key == pygame.K_RIGHT and direccion != "IZQUIERDA":
                        cambio_dir = "DERECHA"

            direccion = cambio_dir
            cabeza = list(snake[0])

            #Calculo hacia dónde se moverán las coordenadas de la nueva cabeza según la tecla presionada
            if direccion == "ARRIBA":
                cabeza[1] -= TAMANO_BLOQUE
            elif direccion == "ABAJO":
                cabeza[1] += TAMANO_BLOQUE
            elif direccion == "IZQUIERDA":
                cabeza[0] -= TAMANO_BLOQUE
            elif direccion == "DERECHA":
                cabeza[0] += TAMANO_BLOQUE

            #Condición de derrota: si la serpiente choca contra los bordes delimitados o contra su propio cuerpo
            if (cabeza[0] < 20 or cabeza[0] >= ANCHO - 20 or 
                cabeza[1] < 40 or cabeza[1] >= ALTO - 20 or 
                cabeza in snake):
                ejecutando = False

            #Agrego la nueva posición de la cabeza al inicio de la lista de la serpiente
            snake.insert(0, cabeza)

            #Verifico si la cabeza colisionó con la comida
            if cabeza == comida:
                puntuacion += 1  # Sumo un punto al marcador
                comida = generar_comida()  # Genero una nueva manzana aleatoria
                # Me aseguro mediante un ciclo que la comida no aparezca encima del cuerpo de la serpiente
                while comida in snake:
                    comida = generar_comida()
            else:
                # Si no comió, elimino el último bloque para mantener el tamaño actual de la serpiente
                snake.pop()

            #Limpio la pantalla pintando el fondo negro de nuevo
            pantalla.fill(NEGRO)
            
            #Dibujo el marco delimitador del área de juego
            pygame.draw.rect(pantalla, COLOR_MARCO, (15, 35, ANCHO - 30, ALTO - 50), 2, border_radius=8)

            #Dibujo los bloques de la serpiente (la cabeza lleva un color diferente para distinguirla visualmente)
            for i, parte in enumerate(snake):
                color_parte = CABEZA_SNAKE if i == 0 else VERDE_SNAKE
                pygame.draw.rect(pantalla, color_parte, (parte[0] + 2, parte[1] + 2, TAMANO_BLOQUE - 4, TAMANO_BLOQUE - 4), border_radius=4)

            #Dibujo la manzana roja con un formato de bloques redondeados muy estéticos
            pygame.draw.rect(pantalla, ROJO_MANZANA, (comida[0] + 2, comida[1] + 2, TAMANO_BLOQUE - 4, TAMANO_BLOQUE - 4), border_radius=6)

            #Renderizo y muestro el marcador de puntuación en la parte superior izquierda
            txt_puntaje = fuente.render(f"PUNTOS: {puntuacion}", True, BLANCO)
            pantalla.blit(txt_puntaje, (25, 10))

            pygame.display.flip()
            reloj.tick(12)  # Controlo la velocidad general del juego a 12 FPS para que sea jugable

    pygame.quit()

if __name__ == "__main__":
    ejecutar_juego()