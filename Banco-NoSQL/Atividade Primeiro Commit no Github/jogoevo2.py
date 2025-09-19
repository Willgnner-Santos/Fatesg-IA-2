import pygame
import sys
import random

pygame.init()

largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Mini Pac-Man Evoluído")

PRETO = (0, 0, 0)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
AZUL = (0, 120, 255)
VERDE = (0, 200, 0)
ROSA = (255, 0, 180)
LARANJA = (255, 140, 0)
VERMELHO = (255, 0, 0)

x, y = 50, 550
velocidade = 6
pacman_tam = 24  # Pac-Man menor para passar em todos os corredores
raio = pacman_tam // 2

# Carregar imagens (Pac-Man menor)
pacman_img = pygame.transform.scale(pygame.image.load("pacman.png"), (pacman_tam, pacman_tam))
fantasma_img = pygame.transform.scale(pygame.image.load("fantasma.png"), (32, 32))
jacare_img = pygame.transform.scale(pygame.image.load("jacare.png"), (32, 32))

# Carregar sons
pygame.mixer.init()
som_ponto = pygame.mixer.Sound("ponto.wav")
som_gameover = pygame.mixer.Sound("gameover.wav")
som_win = pygame.mixer.Sound("win.wav")

# Obstáculos internos melhorados e mais variados (paredes mais finas)
paredes = [
    pygame.Rect(0, 0, largura, 15),             # Topo
    pygame.Rect(0, 0, 15, altura),              # Esquerda
    pygame.Rect(0, altura-15, largura, 15),     # Base
    pygame.Rect(largura-15, 0, 15, altura),     # Direita
    pygame.Rect(100, 100, 400, 7),
    pygame.Rect(100, 200, 7, 200),
    pygame.Rect(200, 300, 200, 7),
    pygame.Rect(500, 100, 7, 200),
    pygame.Rect(100, 500, 400, 7),
    pygame.Rect(300, 400, 7, 100),
    pygame.Rect(200, 150, 200, 7),
    pygame.Rect(400, 250, 7, 100),
    pygame.Rect(150, 350, 100, 7),
    pygame.Rect(350, 150, 7, 100),
    pygame.Rect(250, 450, 100, 7)
]

def ponto_valido(px, py):
    ponto_rect = pygame.Rect(px-7, py-7, 14, 14)
    return not any(ponto_rect.colliderect(p) for p in paredes)

pontos = []
cores_pontos = []
valores_pontos = []

laranja_pos = [(40, 40), (560, 560), (560, 40)]
for pos in laranja_pos:
    if ponto_valido(*pos):
        pontos.append(list(pos))
        cores_pontos.append(LARANJA)
        valores_pontos.append(5)

for _ in range(5):
    while True:
        px = random.randint(30, largura - 30)
        py = random.randint(30, altura - 30)
        if ponto_valido(px, py) and [px, py] not in pontos:
            pontos.append([px, py])
            cores_pontos.append(VERDE)
            valores_pontos.append(3)
            break

for _ in range(5):
    while True:
        px = random.randint(30, largura - 30)
        py = random.randint(30, altura - 30)
        if ponto_valido(px, py) and [px, py] not in pontos:
            pontos.append([px, py])
            cores_pontos.append(AZUL)
            valores_pontos.append(2)
            break

for _ in range(5):
    while True:
        px = random.randint(30, largura - 30)
        py = random.randint(30, altura - 30)
        if ponto_valido(px, py) and [px, py] not in pontos:
            pontos.append([px, py])
            cores_pontos.append(ROSA)
            valores_pontos.append(4)
            break

for _ in range(10):
    while True:
        px = random.randint(30, largura - 30)
        py = random.randint(30, altura - 30)
        if ponto_valido(px, py) and [px, py] not in pontos:
            pontos.append([px, py])
            cores_pontos.append(BRANCO)
            valores_pontos.append(1)
            break

inimigos = [
    {"x": 550, "y": 50, "img": fantasma_img},
    {"x": 550, "y": 550, "img": jacare_img},
    {"x": 300, "y": 300, "img": fantasma_img},
    {"x": 400, "y": 100, "img": jacare_img},
    {"x": 500, "y": 400, "img": fantasma_img}
]

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

score = 0
parar_inimigos_ate = 0

def mostrar_mensagem(texto):
    tela.fill(PRETO)
    mensagem = font.render(texto, True, BRANCO)
    tela.blit(mensagem, (largura//2 - mensagem.get_width()//2, altura//2 - mensagem.get_height()//2))
    pygame.display.flip()
    if "ganhou" in texto:
        som_win.play()
    else:
        som_gameover.play()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    novo_x, novo_y = x, y
    if teclas[pygame.K_LEFT]:
        novo_x -= velocidade
    if teclas[pygame.K_RIGHT]:
        novo_x += velocidade
    pacman_rect_x = pygame.Rect(novo_x - raio, y - raio, pacman_tam, pacman_tam)
    if not any(pacman_rect_x.colliderect(p) for p in paredes):
        x = novo_x

    if teclas[pygame.K_UP]:
        novo_y -= velocidade
    if teclas[pygame.K_DOWN]:
        novo_y += velocidade
    pacman_rect_y = pygame.Rect(x - raio, novo_y - raio, pacman_tam, pacman_tam)
    if not any(pacman_rect_y.colliderect(p) for p in paredes):
        y = novo_y

    tempo_atual = pygame.time.get_ticks()
    inimigos_parados = tempo_atual < parar_inimigos_ate

    for inimigo in inimigos:
        if not inimigos_parados:
            dx = x - inimigo["x"]
            dy = y - inimigo["y"]
            dist = max(1, (dx**2 + dy**2) ** 0.5)
            speed = 3.5
            vel_x = speed * dx / dist
            vel_y = speed * dy / dist

            novo_inimigo_x = inimigo["x"] + vel_x
            novo_inimigo_y = inimigo["y"] + vel_y
            inimigo_rect = pygame.Rect(novo_inimigo_x - 16, novo_inimigo_y - 16, 32, 32)
            if not any(inimigo_rect.colliderect(p) for p in paredes):
                inimigo["x"] = novo_inimigo_x
                inimigo["y"] = novo_inimigo_y
            else:
                temp_x = inimigo["x"] + vel_x
                temp_rect = pygame.Rect(temp_x - 16, inimigo["y"] - 16, 32, 32)
                if not any(temp_rect.colliderect(p) for p in paredes):
                    inimigo["x"] = temp_x
                temp_y = inimigo["y"] + vel_y
                temp_rect = pygame.Rect(inimigo["x"] - 16, temp_y - 16, 32, 32)
                if not any(temp_rect.colliderect(p) for p in paredes):
                    inimigo["y"] = temp_y
                if random.random() < 0.1:
                    inimigo["x"] += random.choice([-speed, speed])
                    inimigo["y"] += random.choice([-speed, speed])

        if inimigo["x"] < 15: inimigo["x"] = 15
        if inimigo["x"] > largura - 15: inimigo["x"] = largura - 15
        if inimigo["y"] < 15: inimigo["y"] = 15
        if inimigo["y"] > altura - 15: inimigo["y"] = altura - 15

    pacman_rect = pygame.Rect(x - raio, y - raio, pacman_tam, pacman_tam)
    for inimigo in inimigos:
        inimigo_rect = pygame.Rect(inimigo["x"] - 16, inimigo["y"] - 16, 32, 32)
        if pacman_rect.colliderect(inimigo_rect):
            mostrar_mensagem("Game Over!")

    tela.fill(PRETO)

    for parede in paredes:
        pygame.draw.rect(tela, AZUL, parede)

    for idx, ponto in enumerate(pontos):
        pygame.draw.circle(tela, cores_pontos[idx], ponto, 7)

    tela.blit(pacman_img, (int(x) - raio, int(y) - raio))

    for inimigo in inimigos:
        tela.blit(inimigo["img"], (int(inimigo["x"]) - 16, int(inimigo["y"]) - 16))

    for idx in range(len(pontos)-1, -1, -1):
        ponto = pontos[idx]
        distancia = ((x - ponto[0]) ** 2 + (y - ponto[1]) ** 2) ** 0.5
        if distancia < raio + 7:
            score += valores_pontos[idx]
            som_ponto.play()
            if cores_pontos[idx] == LARANJA:
                parar_inimigos_ate = pygame.time.get_ticks() + 3000
            del pontos[idx]
            del cores_pontos[idx]
            del valores_pontos[idx]

    texto = font.render(f"Pontos: {score}", True, BRANCO)
    tela.blit(texto, (10, 10))

    if not pontos:
        mostrar_mensagem("Parabéns! Você ganhou o jogo!")

    pygame.display.flip()
    clock.tick(30)