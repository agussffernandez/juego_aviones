import pygame

pygame.init()
pygame.mixer.init()

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



def configurar_pantalla():
    """Configura la pantalla del juego"""
    screen = pygame.display.set_mode((ANCHO, LARGO))
    pygame.display.set_caption("Juego prueba")
    return screen

def cargar_imagenes():
    """Carga las imágenes necesarias para el juego"""
    try:
        jugador_imagen = pygame.image.load("image/avion1.png").convert_alpha()
        enemigo_imagen = pygame.image.load("image/enemigo1.png").convert_alpha()
        fondo_imagen = pygame.image.load("image/fondo2.png")
        fondo_largo = fondo_imagen.get_height()  # Obtiene la altura
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo de imagen. {e}")
        sys.exit(1)
    
    return jugador_imagen, enemigo_imagen, fondo_imagen, fondo_largo


def redimensionar_imagenes(jugador_imagen, enemigo_imagen):
    """Redimensiona las imágenes del jugador y enemigo"""
    jugador_redimension = pygame.transform.scale(jugador_imagen, JUGADOR_REDIMENSION)
    enemigo_redimension = pygame.transform.scale(enemigo_imagen, ENEMIGO_REDIMENSION)
    return jugador_redimension, enemigo_redimension

def inicializar_jugador():
    """Inicializa la posición del jugador"""
    jugador = pygame.Rect(
                        ANCHO // 2 - ANCHO_JUGADOR // 2, 
                        LARGO - ALTO_JUGADOR - 10, ANCHO_JUGADOR,
                        ALTO_JUGADOR
                        )
    return jugador

def reproducir_musica_fondo():
    try:
        pygame.mixer.music.load("audio/fondo.mp3")  # Cargar música de fondo
        pygame.mixer.music.play(loops=-1, start=0.0)  # Reproducir la música de fondo indefinidamente
    except pygame.error as e:
        print(f"Error al cargar la música: {e}")
    
    # Ajusta el volumen de la música (valor entre 0.0 y 1.0)
    pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen al 50%

def cargar_sonidos():
    """Carga los sonidos del juego"""
    try:
        sonido_disparo = pygame.mixer.Sound("audio/disparo.mp3")  # Cargar el sonido de disparo
        sonido_game_over = pygame.mixer.Sound("audio/game_over.mp3")  # Cargar el sonido de Game Over
    except pygame.error as e:
        print(f"Error al cargar los sonidos: {e}")
        sys.exit(1)
    
    return sonido_disparo, sonido_game_over





def main():
    # Configuración inicial
    screen = configurar_pantalla()
    jugador_imagen, enemigo_imagen, fondo_imagen, fondo_largo = cargar_imagenes()
    jugador_redimension, enemigo_redimension = redimensionar_imagenes(jugador_imagen, enemigo_imagen)
    jugador = inicializar_jugador()
    
    # Configuracion sonido
    reproducir_musica_fondo()
    sonido_disparo, sonido_game_over = cargar_sonidos()
    
    
    # Variables del juego
    fondo1 = 0  # Posición vertical del primer fondo
    fondo2 = fondo_largo  # Posición vertical del segundo fondo
    velocidad_fondo = 2  # El fondo se mueve a 2 píxeles hacia abajo
    puntos = 0  # Contador de puntos
    cantidad_enemigos = []  # Almacena los enemigos
    proyectiles = []  # Almacena los proyectiles
    
    # Fuente para mostrar los puntos
    fuente = pygame.font.SysFont(FUENTE, TAM_FUENTE)
    
    # Control de fps
    reloj = pygame.time.Clock()
    
    corriendo = True
    
    while corriendo:
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
        
        mover_jugador(jugador)
        crear_proyectil_con_el_espaciador(proyectiles, jugador, sonido_disparo)
        mover_proyectiles(proyectiles)
        generar_enemigos(cantidad_enemigos)
        mover_enemigos(cantidad_enemigos)
        puntos = detectar_colisiones_entre_proyectiles_y_enemigos(puntos, proyectiles, cantidad_enemigos)
        
        # Terminar el juego si el jugador colisiona con un enemigo
        for enemigo in cantidad_enemigos:
            if jugador.colliderect(enemigo):
                corriendo = False
                sonido_game_over.play()  # Reproducir el sonido de Game Over al terminar el juego
        
        # Llena la pantalla de negro para asegurarse de que no queden imágenes anteriores
        screen.fill(NEGRO)
        
        # Actualiza el movimiento de la imagen de fondo 
        fondo1, fondo2 = actualizar_fondo(fondo1, fondo2, fondo_largo, fondo_imagen, velocidad_fondo, screen)
        
        # Dibujo de los personajes
        screen.blit(jugador_redimension, jugador)
        
        for enemigo in cantidad_enemigos:
            screen.blit(enemigo_redimension, enemigo)
        
        for proyectil in proyectiles:
            pygame.draw.rect(screen, AZUL, proyectil)
        
        # Mostrar puntos en la esquina superior izquierda
        mostrar_puntos = fuente.render(f"Puntos: {puntos}", True, BLANCO)
        screen.blit(mostrar_puntos, (10, 10))
        
        pygame.display.flip()
        
        # Mostrar game over si el juego ha terminado
        if not corriendo:
            pygame.mixer.music.stop()  # Detener la música de fondo al finalizar el juego
            mostrar_game_over(puntos, screen)
            pygame.time.wait(2000)
            corriendo = False
        
        # Control de FPS
        reloj.tick(30)
    
    pygame.quit()

main()