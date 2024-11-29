import pygame

pygame.init()

import random
import sys
from variables.variables import *


#configurar pantalla
screen = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Juego prueba")


# Jugador (Rect)
jugador = pygame.Rect(ANCHO // 2 - ANCHO_JUGADOR // 2, 
                    LARGO - ALTO_JUGADOR - 10, ANCHO_JUGADOR,
                    ALTO_JUGADOR)


# Cargar imágenes
try: 
    jugador_imagen = pygame.image.load("image/avion1.png").convert_alpha()
    enemigo_imagen = pygame.image.load("image/enemigo1.png").convert_alpha()
    fondo_imagen = pygame.image.load("image/fondo2.png")
    fondo_largo = fondo_imagen.get_height()  # Obtiene la altura
except FileNotFoundError as e:
    print(f"Error: No se pudo encontrar el archivo de imagen. {e}")
    sys.exit(1) # Salir del programa si no se encuentran las imágenes

# Redimensionar imágenes
jugador_redimension = pygame.transform.scale(jugador_imagen, JUGADOR_REDIMENSION)
enemigo_redimension = pygame.transform.scale(enemigo_imagen, ENEMIGO_REDIMENSION)

# Fuente
fuente = pygame.font.SysFont(FUENTE, TAM_FUENTE)



# Función para mostrar la pantalla de Game Over
def mostrar_game_over() -> None:
    """ 
    Muestra por pantalla 'game over' y los puntos obtenidos del juego.
    Se llena la pantalla de color negro y se dibujan los textos centrados
    en la pantalla.
    """
    fuente_game_over = pygame.font.SysFont("Arial", 50)
    texto_game_over = fuente_game_over.render("GAME OVER", True, ROJO)
    texto_puntos = fuente_game_over.render(f"Ganaste puntos: {puntos}", True, BLANCO)
    # ANCHO // 2: da el centro horizontal de la pantalla.
    # texto_game_over.get_width() obtiene el ancho del texto "GAME OVER" una vez renderizado
    # texto_game_over.get_width() // 2 obtiene la mitad del ancho del texto.
    # al restarlo de ANCHO // 2, el texto quede centrado horizontalmente.

    # LARGO // 3: calcula un tercio de la altura
    # Esto coloca el texto "GAME OVER" a un tercio de la altura de la pantalla.
    coordenada_rect_game_over = (ANCHO // 2 - texto_game_over.get_width() // 2, LARGO // 3)


    # La misma logica para posicionarlo horizontalmente en el medio (eje x)
    # LARGO // 2: calcula la mitad de altura
    # Esto coloca a "Ganaste puntos: " en el medio
    coordenada_rect_puntos = (ANCHO // 2 - texto_puntos.get_width() // 2, LARGO // 2)
    
    
    # Mostrar el texto
    screen.fill(NEGRO)
    screen.blit(texto_game_over, coordenada_rect_game_over)
    screen.blit(texto_puntos, coordenada_rect_puntos)
    
    pygame.display.flip()

def mover_jugador() -> None:
    """ 
    Mueve al jugador dependiendo de que tecla seleccione.
    
    """
    try: 
        teclas = pygame.key.get_pressed()
        # Movimiento del jugador
        if teclas[pygame.K_LEFT] and jugador.left > 0:
            # Si se presiona la tecla de izquierda, el jugador se mueve 10 píxeles hacia la izquierda
            jugador.x -= 10

        if teclas[pygame.K_RIGHT] and jugador.right < ANCHO:
            # Si se presiona la tecla de derecha, el jugador se mueve 10 píxeles hacia la derecha
            jugador.x += 10

        if teclas[pygame.K_UP] and jugador.top > 0:
            # Si se presiona la tecla hacia arriba, el jugador se mueve 10 píxeles hacia arriba.
            jugador.y -= 10

        if teclas[pygame.K_DOWN] and jugador.bottom < LARGO:
            #Si se presiona la tecla hacia abajo, el jugador se mueve 10 píxeles hacia abajo.
            jugador.y += 10
    except Exception as e:
        print(f"Error al mover al jugador: {e}")


def crear_proyectil_con_el_espaciador(proyectiles: list):
    """ 
    Crea unp proyectil cuando se aprete la barra espaciadora, luego lo
    agrega a la lista de proyectiles
    
    Args:
        proyectiles(list): Lista de proyectiles a agregar proyectil, cada proyectil es .Rect
    """
    try: 
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            # jugador.centerx - 5: ajusta la posicion del proyectil/disparo para que este centrado, pero un poco a la izq
            # jugador. top: es la posición del borde superior del rectángulo que representa al jugador. Posiciona el proyectil justo encima del jugador
            # 5, 5: Estos son los ancho y alto del proyectil.
            proyectil = pygame.Rect(jugador.centerx - 5, jugador.top, 5, 5)  # Creación del proyectil
            proyectiles.append(proyectil)
    except Exception as e:
        print(f"Error al crear proyectil: {e}")


def mover_proyectiles(proyectiles: list):
    """  
    Mueve a los proyectiles hacia arriba (10 pixeles) y elimina
    aquellos que hayan salido de la pantalla
    
    Args:
        proyectiles(list): Lista de proyectiles a eliminar proyectil, cada proyectil es .Rect
    """
    try:
        for proyectil in proyectiles[:]:
            """
            El bucle recorre todos los proyectiles actuales en la lista proyectiles. 
            El uso de [:] hace que estemos iterando sobre una copia de la lista, 
            lo que permite modificar la lista (eliminando elementos) sin causar problemas durante la iteración.
            """
            # proyectil.y: es un atributo del proyectl(que es de calse rect), indica la coordenada eje Y
            proyectil.y -= 10
            # proyectil.button: es la coordenada Y de la parte inferior del rectángulo
            # Verifica si la parte inferior del proyectil ha salido de la pantalla
            if proyectil.bottom < 0: # la pantalla tiene un límite superior (Y = 0)
                proyectiles.remove(proyectil)
    except Exception as e:
        print(f"Error al mover proyectiles: {e}")


def generar_enemigos(cantidad_enemigos: list) -> None:
    """ 
    Genera un enemigo de clase Rect, y lo agrega a la lista cantidad_enemigos, solo si
    la lista cantidad_enemigos tiene menos de 10 enemigos.
    Es decir, en el juego puede haber hasta 10 enemigos a la vez

    Args:
        cantidad_enemigos(list): Lista con todos los enemigos (max. 10), cada enemigo es .Rect
    """
    if len(cantidad_enemigos) < 10:
        enemigo = pygame.Rect(random.randint(0, ANCHO - ANCHO_ENEMIGOS), 
                            0, ANCHO_ENEMIGOS, ALTO_ENEMIGOS)
        cantidad_enemigos.append(enemigo)

def mover_enemigos(cantidad_enemigos: list) -> None:
    """  
    Mueve al enemigo 5 pixeles hacia abajo verticalmente (eje y) y
    cuando salen de pantalla, los elimina de la lista cantidad_enemigos
    
    Args:
        cantidad_enemigos(list): Lista con todos los enemigos (max. 10), cada enemigo es .Rect
    """
    try:
        for enemigo in cantidad_enemigos:
            # enemigo.y: atributo de la clase Rect, que indica la coordenada del eje y del objeto
            enemigo.y += 5 
            # enemigo.top: indica la coordenada Y de la parte superior de la imagen/rectangulo enemigo
            # LARGO: altura de la pantalla
            if enemigo.top > LARGO:  # Si la parte superior del enemigo ha cruzado la parte inferior de la pantalla
                cantidad_enemigos.remove(enemigo)  # Elimina al enemigo de la lista
    except Exception as e:
        print(F"Error al mover enemigos: {e}")


def detectar_colisiones_entre_proyectiles_y_enemigos(puntos: int, proyectiles: list, cantidad_enemigos: list) -> int:
    """  
    Detecta colisiones entre proyectiles y enemigos, y si es asi:
    -> Se le suman 5 puntos al jugador
    -> El enemigo de elimina
    """
    try:
        for proyectil in proyectiles[:]:
            # Recorre 1 indice de proyectiles, recorre todos los objetos de la lista enemigos
            for enemigo in cantidad_enemigos[:]:
                # Verifica si el proyectil choco con algún enemigo de la lista cantidad_enemigos
                if proyectil.colliderect(enemigo):
                    proyectiles.remove(proyectil)
                    cantidad_enemigos.remove(enemigo)
                    puntos += 5
                    # Luego de encontrar la colision, sale del bucle
                    break
    except Exception as e:
        print(f"Error al detectar colisiones entre proyectiles y enemigos: {e}")
    return puntos


def actualizar_fondo(fondo1: int, fondo2: int, velocidad_fondo: float) -> tuple[int,int]:
    """ 
    
    """
    try:    
        # A las pociones verticales(fondo1, fondo2), se le suman 2 pixeles
        # Con la suma hara que se dezplacen hacia abajo
        fondo1 += velocidad_fondo
        fondo2 += velocidad_fondo

        # Pega en la pantalla los fondos y genera el movimiento
        # Dibuja fondo_imagen en la posicion (x = 0, y=fondo1)
        # A medida que fondo1 aumenta, la imagen de fondo se mueve hacia abajo en la pantalla.
        screen.blit(fondo_imagen, (0, fondo1))
        screen.blit(fondo_imagen, (0, fondo2))

        # Verifica si la posicion en la que este fondo 1 ha llegado o ha pasado la altura de la imagen de fondo(fondo_largo)
        # Es decir, si el fondo ya paso hacia abajo, salio completamente de la pantalla por la parte inferior, y ya no es visible
        if fondo1 >= fondo_largo:
            # Entonces si se ha movido completamente fuera de la pantalla
            # Actualiza su posición a una negativa en el eje Y
            # Es decir, actualiza su eje Y justo por encima de la pantalla
            fondo1 = -fondo_largo
        if fondo2 >= fondo_largo:
            fondo2 = -fondo_largo
        return fondo1, fondo2
    except Exception as e:
        print(f"Error al actualizar el fondo: {e}")
        return fondo1, fondo2  # Si ocurre un error, devuelve los valores originales



# Variables para el juego

# control de fps
reloj = pygame.time.Clock()

# contador puntos
puntos = 0

# fondo
fondo1 = 0 # Posicion vertical del primer fondo (y =parte superior de la pantalla) 
fondo2 = fondo_largo # Posicion vertical del segundo fondo (y = el largo del fondo)
velocidad_fondo = 2 #El fondo se movera a 2 pixeles hacia abajo

# 
cantidad_enemigos = []

# Crear proyectiles
proyectiles = []



#Bucle
corriendo = True

while corriendo:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    
    mover_jugador()
    crear_proyectil_con_el_espaciador(proyectiles)
    mover_proyectiles(proyectiles)
    generar_enemigos(cantidad_enemigos)
    mover_enemigos(cantidad_enemigos)
    puntos = detectar_colisiones_entre_proyectiles_y_enemigos(puntos, proyectiles, cantidad_enemigos)

    # Terminar el juego si el jugador colisiona con un enemigo
    for enemigo in cantidad_enemigos:
        if jugador.colliderect(enemigo):
            corriendo = False

    # Llena la pantalla de negro para asegurarse de que no queden imagenes anteriores
    screen.fill(NEGRO)

    # Actualiza el movimiento de la imagen de fondo 
    fondo1, fondo2 = actualizar_fondo(fondo1, fondo2, velocidad_fondo)


    # DIBUJO DE LOS PERSONAJES

    #jugador imagen
    # En la pantalla, dibuja la imagen redimensionada sobre el rect del jugador
    screen.blit(jugador_redimension, jugador)

    # recorre cada enemigo en la lista cantidad_enemigos
    for enemigo in cantidad_enemigos:
        #enemigo imagen
        # Dibuja la imagen redimensionada del enemigo, sobre los rect que guarda cada posicion que se va iterando
        screen.blit(enemigo_redimension, enemigo)

    # Dibujar proyectiles
    # Recorre todos proyectiles de la lista proyectiles
    for proyectil in proyectiles:
        # Dibuja un rectangulo azul para representar cada proyectil en su posicion correspondiente(definida por los rect)
        pygame.draw.rect(screen, AZUL, proyectil)
 

    # Mostrar puntos arriba a la izq
    # utiliza la fuente definida al principio y crea una imagen de texto de color blanco
    mostrar_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
    # Pega el el texto en la esquina superior izquiera
    screen.blit(mostrar_puntos,(10, 10))

    pygame.display.flip()

    # Mostrar game over si el juego ha terminado
    if not corriendo:
        mostrar_game_over()  # Mostrar pantalla de Game Over
        pygame.time.wait(2000)  # Esperar 2 segundos para que se vea el Game Over
        corriendo = False  # Termina el juego

    # controla la tasa de actualización del juego, limitando el bucle a 30 fotogramas por segundo (FPS)
    reloj.tick(30)

pygame.quit()