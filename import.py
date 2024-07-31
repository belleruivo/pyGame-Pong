import pygame
import pygame.freetype  # para usar fontes externas

pygame.init()  # inicializa todos os módulos do pygame, necessários para o jogo

LARGURA, ALTURA = 700, 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")

# define a taxa de atualização do jogo, em frames por segundo
FPS = 60

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 128, 0)  # Cor verde mais escura e sutil para o fundo da mensagem de vitória

LARGURA_RAQUETE, ALTURA_RAQUETE = 15, 100  # Largura das raquetes diminuída
RAIO_BOLA = 7
RAIO_BORDA_RAQUETE = 10  # raio das bordas arredondadas da raquete

# Configura a fonte para a pontuação
FONTE_PONTUACAO = pygame.freetype.SysFont("freesansbold", 50)

# Configura a fonte para os nomes dos jogadores
FONTE_JOGADORES = pygame.freetype.SysFont("freesansbold", 30)  # Fonte menor para os nomes dos jogadores

# Configura a fonte para a mensagem de vitória
FONTE_VITORIA = pygame.freetype.SysFont("freesansbold", 60)  # Fonte maior para a mensagem de vitória
FONTE_REINICIO = pygame.freetype.SysFont("freesansbold", 40)  # Fonte para a mensagem de reinício

PONTUACAO_VITORIA = 10

class Raquete:
    COR = BRANCO
    VELOCIDADE = 5

    def __init__(self, x, y, largura, altura):
        self.x = self.x_original = x
        self.y = self.y_original = y
        self.largura = largura
        self.altura = altura

    def desenhar(self, tela):
        # desenha a raquete na tela com bordas arredondadas
        pygame.draw.rect(tela, self.COR, (self.x, self.y, self.largura, self.altura), border_radius=RAIO_BORDA_RAQUETE)
        
    def mover(self, cima=True):
        if cima:
            self.y -= self.VELOCIDADE
        else:
            self.y += self.VELOCIDADE

    def resetar(self):
        self.x = self.x_original
        self.y = self.y_original

class Bola:
    VELOCIDADE_MAX = 7
    COR = BRANCO

    def __init__(self, x, y, raio):
        self.x = self.x_original = x
        self.y = self.y_original = y
        self.raio = raio
        self.velocidade_x = self.VELOCIDADE_MAX
        self.velocidade_y = 0

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.COR, (self.x, self.y), self.raio)

    def mover(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

    def resetar(self):
        self.x = self.x_original
        self.y = self.y_original
        self.velocidade_y = 0
        self.velocidade_x *= -1

def desenhar(tela, raquetes, bola, pontuacao_esquerda, pontuacao_direita, mensagem_reiniciar=None, mensagem_vitoria=None):
    tela.fill(PRETO)

    # cria a pontuação dos jogadores e a exibe na tela
    texto_pontuacao_esquerda, retangulo_esquerda = FONTE_PONTUACAO.render(f"{pontuacao_esquerda}", BRANCO)
    texto_pontuacao_direita, retangulo_direita = FONTE_PONTUACAO.render(f"{pontuacao_direita}", BRANCO)
    
    tela.blit(texto_pontuacao_esquerda, (LARGURA // 4 - retangulo_esquerda.width // 2, 60))  # Distância ajustada
    tela.blit(texto_pontuacao_direita, (LARGURA * (3 / 4) - retangulo_direita.width // 2, 60))  # Distância ajustada

    # desenha todas as raquetes
    for raquete in raquetes:
        raquete.desenhar(tela)

    # desenha a linha divisória no meio da tela
    for i in range(10, ALTURA, ALTURA // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(tela, BRANCO, (LARGURA // 2 - 5, i, 5, ALTURA // 20))

    # desenha a bola na tela
    bola.desenhar(tela)

    # Adiciona o texto do jogador
    texto_jogador1, retangulo_jogador1 = FONTE_JOGADORES.render("Player 1", BRANCO)
    texto_jogador2, retangulo_jogador2 = FONTE_JOGADORES.render("Player 2", BRANCO)
    tela.blit(texto_jogador1, (LARGURA // 4 - retangulo_jogador1.width // 2, 10))  # Distância ajustada
    tela.blit(texto_jogador2, (LARGURA * (3 / 4) - retangulo_jogador2.width // 2, 10))  # Distância ajustada

    if mensagem_vitoria:
        texto_vitoria, retangulo_vitoria = FONTE_VITORIA.render(mensagem_vitoria, BRANCO)
        fundo_mensagem = pygame.Surface(retangulo_vitoria.size)
        fundo_mensagem.fill(VERDE)
        fundo_mensagem.set_alpha(200)  # Define a transparência do fundo
        tela.blit(fundo_mensagem, (LARGURA // 2 - retangulo_vitoria.width // 2, ALTURA // 2 - retangulo_vitoria.height // 2 - 50))
        tela.blit(texto_vitoria, (LARGURA // 2 - retangulo_vitoria.width // 2, ALTURA // 2 - retangulo_vitoria.height // 2 - 50))

    if mensagem_reiniciar:
        texto_reiniciar, retangulo_reiniciar = FONTE_REINICIO.render(mensagem_reiniciar, BRANCO)
        tela.blit(texto_reiniciar, (LARGURA // 2 - retangulo_reiniciar.width // 2, ALTURA // 2 - retangulo_reiniciar.height // 2 + 50))

    pygame.display.update()

def tratar_colisao(bola, raquete_esquerda, raquete_direita):
    if bola.y + bola.raio >= ALTURA:
        bola.velocidade_y *= -1
    elif bola.y - bola.raio <= 0:
        bola.velocidade_y *= -1

    if bola.velocidade_x < 0:
        if bola.y >= raquete_esquerda.y and bola.y <= raquete_esquerda.y + raquete_esquerda.altura:
            if bola.x - bola.raio <= raquete_esquerda.x + raquete_esquerda.largura:
                bola.velocidade_x *= -1

                meio_y = raquete_esquerda.y + raquete_esquerda.altura / 2
                diferenca_y = meio_y - bola.y
                fator_reducao = (raquete_esquerda.altura / 2) / bola.VELOCIDADE_MAX
                vel_y = diferenca_y / fator_reducao
                bola.velocidade_y = -1 * vel_y

    else:
        if bola.y >= raquete_direita.y and bola.y <= raquete_direita.y + raquete_direita.altura:
            if bola.x + bola.raio >= raquete_direita.x:
                bola.velocidade_x *= -1

                meio_y = raquete_direita.y + raquete_direita.altura / 2
                diferenca_y = meio_y - bola.y
                fator_reducao = (raquete_direita.altura / 2) / bola.VELOCIDADE_MAX
                vel_y = diferenca_y / fator_reducao
                bola.velocidade_y = -1 * vel_y

def tratar_movimento_raquetes(teclas, raquete_esquerda, raquete_direita):
    if teclas[pygame.K_w] and raquete_esquerda.y - raquete_esquerda.VELOCIDADE >= 0:
        raquete_esquerda.mover(cima=True)
    if teclas[pygame.K_s] and raquete_esquerda.y + raquete_esquerda.VELOCIDADE + raquete_esquerda.altura <= ALTURA:
        raquete_esquerda.mover(cima=False)

    if teclas[pygame.K_UP] and raquete_direita.y - raquete_direita.VELOCIDADE >= 0:
        raquete_direita.mover(cima=True)
    if teclas[pygame.K_DOWN] and raquete_direita.y + raquete_direita.VELOCIDADE + raquete_direita.altura <= ALTURA:
        raquete_direita.mover(cima=False)

def main():
    raquete_esquerda = Raquete(10, ALTURA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE)
    raquete_direita = Raquete(LARGURA - 10 - LARGURA_RAQUETE, ALTURA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE)
    bola = Bola(LARGURA // 2, ALTURA // 2, RAIO_BOLA)

    pontuacao_esquerda = 0
    pontuacao_direita = 0

    clock = pygame.time.Clock()
    rodando = True
    jogo_terminado = False
    vencedor = None

    while rodando:
        clock.tick(FPS)
        mensagem_reiniciar = None
        mensagem_vitoria = None
        if jogo_terminado:
            mensagem_reiniciar = "TECLE ENTER PARA JOGAR NOVAMENTE"
            if vencedor:
                mensagem_vitoria = f"{vencedor} VENCEU!"
        desenhar(TELA, [raquete_esquerda, raquete_direita], bola, pontuacao_esquerda, pontuacao_direita, mensagem_reiniciar, mensagem_vitoria)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                break

            if jogo_terminado:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                    bola.resetar()
                    raquete_esquerda.resetar()
                    raquete_direita.resetar()
                    pontuacao_esquerda = 0
                    pontuacao_direita = 0
                    jogo_terminado = False
                    vencedor = None

        if jogo_terminado:
            continue

        teclas = pygame.key.get_pressed()
        tratar_movimento_raquetes(teclas, raquete_esquerda, raquete_direita)

        bola.mover()
        tratar_colisao(bola, raquete_esquerda, raquete_direita)

        if bola.x < 0:
            pontuacao_direita += 1
            bola.resetar()
        elif bola.x > LARGURA:
            pontuacao_esquerda += 1
            bola.resetar()

        if pontuacao_esquerda >= PONTUACAO_VITORIA:
            jogo_terminado = True
            vencedor = "PLAYER 1"
        elif pontuacao_direita >= PONTUACAO_VITORIA:
            jogo_terminado = True
            vencedor = "PLAYER 2"

    pygame.quit()

if __name__ == '__main__':
    main()
