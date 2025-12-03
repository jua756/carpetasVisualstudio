import pygame
import random
import sys

# 1. INICIALIZACIÓN
pygame.init()

# 2. VARIABLES DE CONFIGURACIÓN (VENTANA)
ANCHO = 500
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego simple con arrays")

# 3. VARIABLES DEL JUGADOR
player_x = ANCHO // 2  # Posición inicial X (centro)
player_y = ALTO - 50   # Posición inicial Y (cerca del borde inferior)
player_size = 40       # Tamaño (lado del cuadrado)
player_vel = 5         # Velocidad de movimiento

# 4. ESTRUCTURA DE DATOS (ARRAY/LISTA)
# Contendrá la información de cada obstáculo: [x, y, tamaño, velocidad]
obstaculos = []

# 5. VARIABLES DE CONTROL
clock = pygame.time.Clock()
running = True  # Controla el BUCLE PRINCIPAL

# 6. BUCLE PRINCIPAL (Game Loop)
while running:  # BUCLE WHILE para mantener el juego activo
    # Limita la velocidad del bucle a 60 cuadros por segundo
    clock.tick(60)

    # GESTIÓN DE EVENTOS
    for e in pygame.event.get():  # BUCLE FOR para procesar eventos
        if e.type == pygame.QUIT:  # CONDICIONAL IF: Si el usuario cierra la ventana
            running = False

    # MOVIMIENTO DEL JUGADOR
    teclas = pygame.key.get_pressed()  # Obtiene el estado de todas las teclas

    # CONDICIONAL IF: Mover a la izquierda
    if teclas[pygame.K_LEFT]:
        player_x -= player_vel

    # CONDICIONAL IF: Mover a la derecha (separado del anterior)
    if teclas[pygame.K_RIGHT]:
        player_x += player_vel

    # LÍMITES DE PANTALLA (CONDICIONALES para evitar que el jugador se salga)
    if player_x < 0:
        player_x = 0
    if player_x > ANCHO - player_size:
        player_x = ANCHO - player_size

    # CREACIÓN DE OBSTÁCULOS
    # CONDICIONAL IF: Se crea un nuevo obstáculo basado en una probabilidad baja
    if random.random() < 0.02:
        x = random.randint(0, ANCHO - 30)
        y = -30
        tamaño = 30
        vel = 4
        # AGREGADO AL ARRAY (Lista) de obstáculos
        obstaculos.append([x, y, tamaño, vel])

    # ACTUALIZAR POSICIÓN DE OBSTÁCULOS
    for obs in obstaculos:  # BUCLE FOR para mover cada obstáculo
        obs[1] += obs[3]  # obs[1] es la 'y', obs[3] es la 'vel'

    # LIMPIEZA DE OBSTÁCULOS
    # BUCLE INTERNO (List comprehension) + CONDICIONAL para eliminar los que salen de la pantalla
    obstaculos = [o for o in obstaculos if o[1] < ALTO + 40]

    # COMPROBACIÓN DE COLISIONES
    jugador_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    
    for o in obstaculos:  # BUCLE FOR para revisar colisión con cada obstáculo
        obs_rect = pygame.Rect(o[0], o[1], o[2], o[2])
        
        if jugador_rect.colliderect(obs_rect):  # CONDICIONAL IF: Detección de colisión
            print("GAME OVER")
            running = False # Opcional: Para salir del bucle
            pygame.quit()
            sys.exit() # Terminación forzada del programa para cerrar la ventana

    # 7. DIBUJO EN PANTALLA
    pantalla.fill((20, 20, 20)) # Fondo oscuro
    
    # Dibujar jugador
    pygame.draw.rect(pantalla, (100, 255, 255), (player_x, player_y, player_size, player_size))
    
    # Dibujar obstáculos
    for o in obstaculos:  # BUCLE FOR para dibujar todos los obstáculos
        pygame.draw.rect(pantalla, (255, 100, 100), (o[0], o[1], o[2], o[2]))
        
    # Actualiza la pantalla para mostrar lo que se ha dibujado
    pygame.display.flip()

# 8. SALIDA DEL JUEGO
pygame.quit()
