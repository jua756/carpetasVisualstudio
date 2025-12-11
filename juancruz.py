import pygame
import random
import sys

pygame.init()

# -------------------------
# CONFIGURACIÓN DE VENTANA
# -------------------------
ANCHO = 500
ALTO = 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego simple con arrays")

clock = pygame.time.Clock()

# -------------------------
# VARIABLES DEL JUGADOR
# -------------------------
player_size = 40
player_vel = 5

# -------------------------
# ESTADOS DEL JUEGO
# -------------------------
STATE_MENU = 0
STATE_VOCAB = 1
STATE_PLAYING = 2
STATE_GAME_OVER = 3
game_state = STATE_MENU

# -------------------------
# FUNCIÓN PARA REINICIAR
# -------------------------
def reset_game():
    global player_x, player_y, obstaculos
    player_x = ANCHO // 2
    player_y = ALTO - 50
    obstaculos = []

reset_game()

# Lista de vocabulario
vocabulario = [
    "Start = Comenzar",
    "Exit = Salir",
    "Game Over = Fin del juego",
    "Move Left = Mover a la izquierda",
    "Move Right = Mover a la derecha",
    "Left Arrow = Flecha izquierda",
    "Right Arrow = Flecha derecha"
]

running = True

# -------------------------
# LOOP PRINCIPAL
# -------------------------
while running:
    clock.tick(60)

    # EVENTOS
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        # TECLA ESC → salir
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        # -------------------------
        # ESTADO: MENU INICIAL
        # -------------------------
        if game_state == STATE_MENU:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                game_state = STATE_VOCAB  # primero se muestra vocabulario

        # -------------------------
        # ESTADO: VOCABULARIO
        # -------------------------
        elif game_state == STATE_VOCAB:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                game_state = STATE_PLAYING

        # -------------------------
        # ESTADO: GAME OVER
        # -------------------------
        elif game_state == STATE_GAME_OVER:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                reset_game()
                game_state = STATE_PLAYING

    # -------------------------
    # ESTADO: JUGANDO
    # -------------------------
    if game_state == STATE_PLAYING:

        teclas = pygame.key.get_pressed()

        # Movimiento del jugador
        if teclas[pygame.K_LEFT]:
            player_x -= player_vel
        if teclas[pygame.K_RIGHT]:
            player_x += player_vel

        # Límites
        if player_x < 0:
            player_x = 0
        if player_x > ANCHO - player_size:
            player_x = ANCHO - player_size

        # Crear obstáculos
        if random.random() < 0.02:
            x = random.randint(0, ANCHO - 30)
            y = -30
            tamaño = 30
            vel = 4
            obstaculos.append([x, y, tamaño, vel])

        # Mover obstáculos
        for obs in obstaculos:
            obs[1] += obs[3]

        # Limpiar obstáculos fuera de pantalla
        obstaculos = [o for o in obstaculos if o[1] < ALTO + 40]

        # Colisiones
        jugador_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        for o in obstaculos:
            obs_rect = pygame.Rect(o[0], o[1], o[2], o[2])
            if jugador_rect.colliderect(obs_rect):
                game_state = STATE_GAME_OVER

    # -------------------------
    # DIBUJADO EN PANTALLA
    # -------------------------
    pantalla.fill((20, 20, 20))
    font = pygame.font.SysFont(None, 32)

    # -------------------------
    # PANTALLA MENU
    # -------------------------
    if game_state == STATE_MENU:
        texto = font.render("Press SPACE to start", True, (255, 255, 255))
        pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, ALTO//2))

    # -------------------------
    # PANTALLA VOCABULARIO
    # -------------------------
    elif game_state == STATE_VOCAB:
        y_offset = 80
        title = font.render("VOCABULARY LIST:", True, (255, 255, 0))
        pantalla.blit(title, (20, 20))

        for palabra in vocabulario:
            linea = font.render(palabra, True, (255, 255, 255))
            pantalla.blit(linea, (20, y_offset))
            y_offset += 40

        msg = font.render("Press ENTER to close the vocabulary list", True, (150, 200, 255))
        pantalla.blit(msg, (20, ALTO - 60))

    # -------------------------
    # PANTALLA DEL JUEGO
    # -------------------------
    elif game_state == STATE_PLAYING:
        pygame.draw.rect(pantalla, (100, 255, 255), (player_x, player_y, player_size, player_size))

        for o in obstaculos:
            pygame.draw.rect(pantalla, (255, 100, 100), (o[0], o[1], o[2], o[2]))

    # -------------------------
    # PANTALLA GAME OVER
    # -------------------------
    elif game_state == STATE_GAME_OVER:
        txt = font.render("GAME OVER", True, (255, 50, 50))
        pantalla.blit(txt, (ANCHO//2 - txt.get_width()//2, ALTO//2 - 40))

        txt2 = font.render("Press SPACE to play again", True, (255, 255, 255))
        pantalla.blit(txt2, (ANCHO//2 - txt2.get_width()//2, ALTO//2 + 10))

    pygame.display.flip()

pygame.quit()
