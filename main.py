import pygame

pygame.init()

import sys
from variables.constantes import *
from funciones.mostrar_game_over import *
from funciones.mover_jugador import *
from funciones.crear_proyectil import *
from funciones.mover_proyectiles import *
from funciones.generar_enemigos import *
from funciones.mover_enemigos import *
from funciones.detectar_colisiones import *
from funciones.actualizar_fondo import *


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
    
    mover_jugador(jugador)
    crear_proyectil_con_el_espaciador(proyectiles, jugador)
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
    fondo1, fondo2 = actualizar_fondo(fondo1, fondo2,fondo_largo, fondo_imagen, velocidad_fondo, screen)
    
    
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
        mostrar_game_over(puntos, screen)  # Mostrar pantalla de Game Over
        pygame.time.wait(2000)  # Esperar 2 segundos para que se vea el Game Over
        corriendo = False  # Termina el juego
    
    
    # controla la tasa de actualización del juego, limitando el bucle a 30 fotogramas por segundo (FPS)
    reloj.tick(30)

pygame.quit()