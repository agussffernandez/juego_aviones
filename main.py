import pygame
import random

pygame.init()

#configurar pantalla
ANCHO = 600
LARGO = 800
screen = pygame.display.set_mode((ANCHO, LARGO))
pygame.display.set_caption("Juego prueba")

#colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE =(0, 255, 0)

#jugador
ANCHO_JUGADOR = 50
ALTO_JUGADOR = 50
jugador = pygame.Rect(ANCHO // 2 - ANCHO_JUGADOR // 2, 
                    LARGO - ALTO_JUGADOR - 10, ANCHO_JUGADOR,
                    ALTO_JUGADOR)

#enemigos
ANCHO_ENEMIGOS = 30
ALTO_ENEMIGOS = 30

#imagenes
jugador_imagen = pygame.image.load("avion1.png").convert_alpha()
enemigo_imagen = pygame.image.load("enemigo1.png").convert_alpha()
fondo_imagen = pygame.image.load("fondo2.png")
fondo_largo = fondo_imagen.get_height() #Obtiene la altura

#definir nuevas dimensiones
JUGADOR_REDIMENSION = (50, 50)
ENEMIGO_REDIMENSION = (30, 30)

#redimension de imagen

jugador_redimension = pygame.transform.scale(jugador_imagen, JUGADOR_REDIMENSION)
enemigo_redimension = pygame.transform.scale(enemigo_imagen, ENEMIGO_REDIMENSION)


# tipo de fuente y tamaño
fuente = pygame.font.SysFont("Arial", 24)


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


def crear_proyectil_con_el_espaciador(proyectiles: list):
    """ 
    Si se apreta un espacio, crea un proyectil y lo agrega a la lista proyectil
    Agrega

    """
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_SPACE]:
        # jugador.centerx - 5: ajusta la posicion del proyectil/disparo para que este centrado, pero un poco a la izq
        # jugador. top: es la posición del borde superior del rectángulo que representa al jugador. Posiciona el proyectil justo encima del jugador
        # 5, 5: Estos son los ancho y alto del proyectil.
        proyectil = pygame.Rect(jugador.centerx - 5, jugador.top, 5, 5)  # Creación del proyectil
        proyectiles.append(proyectil)


def mover_proyectiles(proyectiles: list):
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


def generar_enemigos(cantidad_enemigos: list) -> None:
    """ 
     Genera un enemigo de clase Rect, y lo agrega a la lista cantidad_enemigos, solo si
     la lista cantidad_enemigos tiene menos de 10 enemigos.
     Es decir, en el juego puede haber hasta 10 enemigos a la vez

    """
    if len(cantidad_enemigos) < 10:
        enemigo = pygame.Rect(random.randint(0, ANCHO - ANCHO_ENEMIGOS), 
                              0, ANCHO_ENEMIGOS, ALTO_ENEMIGOS)
        cantidad_enemigos.append(enemigo)

def mover_enemigos(cantidad_enemigos: list) -> None:
    """  
    Mueve al enemigo 5 pixeles hacia abajo verticalmente (eje y) y
    cuando salen de pantalla, los elimina de la lista cantidad_enemigos
    """
    for enemigo in cantidad_enemigos:
        # enemigo.y: atributo de la clase Rect, que indica la coordenada del eje y del objeto
        enemigo.y += 5 
        # enemigo.top: indica la coordenada Y de la parte superior de la imagen/rectangulo enemigo
        # LARGO: altura de la pantalla
        if enemigo.top > LARGO:  # Si la parte superior del enemigo ha cruzado la parte inferior de la pantalla
            cantidad_enemigos.remove(enemigo)  # Elimina al enemigo de la lista



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


    # Detectar colisiones entre proyectiles y enemigos
    for proyectil in proyectiles[:]:
        """
        El bucle recorre todos los proyectiles actuales en la lista proyectiles. 
        El uso de [:] hace que estemos iterando sobre una copia de la lista, 
        lo que permite modificar la lista (eliminando elementos) sin causar problemas durante la iteración.
        """
        for enemigo in cantidad_enemigos[:]:
            if proyectil.colliderect(enemigo):  # Si hay colisión entre el disparo y el enemigo
                proyectiles.remove(proyectil)  # Elimina el proyectil
                cantidad_enemigos.remove(enemigo)  # Elimina el enemigo
                puntos += 5  # Aumenta los puntos por eliminar un enemigo
                break

    # Terminar el juego si el jugador colisiona con un enemigo
    for enemigo in cantidad_enemigos:
        if jugador.colliderect(enemigo):
            corriendo = False

    # Llena la pantalla de negro para asegurarse de que no queden imagenes anteriores
    screen.fill(NEGRO)

    # Movimiento de la imagen de fondo

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
        # Entonces si se ha movimo completamente fuera de la pantalla
        # Actualiza su posición negativa en el eje Y
        # Es decir, justo por encima de la pantalla
        fondo1 = -fondo_largo
    if fondo2 >= fondo_largo:
        fondo2 = -fondo_largo


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