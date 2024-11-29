import pygame
import sys

#configurar pantalla
ANCHO = 600
LARGO = 800
screen = pygame.display.set_mode((ANCHO, LARGO))


#colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE =(0, 255, 0)

#jugador
ANCHO_JUGADOR = 50
ALTO_JUGADOR = 50

#jugador(Rect)

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