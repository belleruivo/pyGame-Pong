import pygame
import pygame.freetype  # para usar fontes externas

pygame.init()  # inicializa todos os módulos do pygame, necessários para o jogo

LARGURA, ALTURA = 700, 500  # define a largura e a altura da tela
TELA = pygame.display.set_mode((LARGURA, ALTURA))  # cria a tela com as dimensões especificadas
pygame.display.set_caption("Pong")  # define o título da janela do jogo

# define a taxa de atualização do jogo, em frames por segundo
FPS = 60

# define cores em RGB
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)

# define dimensões das raquetes e da bola
LARGURA_RAQUETE, ALTURA_RAQUETE = 15, 100  # largura das raquetes diminuída
RAIO_BOLA = 7
RAIO_BORDA_RAQUETE = 10  # raio das bordas arredondadas da raquete

# configura a fonte para a pontuação
FONTE_PONTUACAO = pygame.freetype.SysFont("freesansbold", 50)

# configura a fonte para os nomes dos jogadores
FONTE_JOGADORES = pygame.freetype.SysFont("freesansbold", 30)  # fonte menor para os nomes dos jogadores

# configura a fonte para a mensagem de vitória
FONTE_VITORIA = pygame.freetype.SysFont("freesansbold", 40)  # fonte maior para a mensagem de vitória
FONTE_REINICIO = pygame.freetype.SysFont("freesansbold", 20)  # fonte para a mensagem de reinício

PONTUACAO_VITORIA = 10  # define a pontuação necessária para vencer

class Raquete:
    VELOCIDADE = 5  # define a velocidade de movimento das raquetes

    def __init__(self, x, y, largura, altura, cor):
        self.x = self.x_original = x  # posição x inicial
        self.y = self.y_original = y  # posição y inicial
        self.largura = largura  # largura da raquete
        self.altura = altura  # altura da raquete
        self.COR = cor  # cor da raquete

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.COR, (self.x, self.y, self.largura, self.altura), border_radius=RAIO_BORDA_RAQUETE)  # desenha a raquete com bordas arredondadas

    def mover(self, cima=True):
        if cima:
            self.y -= self.VELOCIDADE  # move a raquete para cima
        else:
            self.y += self.VELOCIDADE  # move a raquete para baixo

    def resetar(self):
        self.x = self.x_original  # reseta a posição x da raquete
        self.y = self.y_original  # reseta a posição y da raquete

class Bola:
    VELOCIDADE_MAX = 7  # define a velocidade máxima da bola
    COR = BRANCO  # define a cor da bola

    def __init__(self, x, y, raio):
        self.x = self.x_original = x  # posição x inicial
        self.y = self.y_original = y  # posição y inicial
        self.raio = raio  # raio da bola
        self.velocidade_x = self.VELOCIDADE_MAX  # velocidade inicial no eixo x
        self.velocidade_y = 0  # velocidade inicial no eixo y

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.COR, (self.x, self.y), self.raio)  # desenha a bola

    def mover(self):
        self.x += self.velocidade_x  # move a bola no eixo x
        self.y += self.velocidade_y  # move a bola no eixo y

    def resetar(self):
        self.x = self.x_original  # reseta a posição x da bola
        self.y = self.y_original  # reseta a posição y da bola
        self.velocidade_y = 0  # reseta a velocidade no eixo y
        self.velocidade_x *= -1  # inverte a direção da bola no eixo x

def desenhar(tela, raquetes, bola, pontuacao_esquerda, pontuacao_direita, mensagem_reiniciar=None, mensagem_vitoria=None):
    tela.fill(PRETO)  # preenche a tela com a cor preta

    # cria a pontuação dos jogadores e a exibe na tela
    texto_pontuacao_esquerda, retangulo_esquerda = FONTE_PONTUACAO.render(f"{pontuacao_esquerda}", BRANCO)
    texto_pontuacao_direita, retangulo_direita = FONTE_PONTUACAO.render(f"{pontuacao_direita}", BRANCO)
    
    tela.blit(texto_pontuacao_esquerda, (LARGURA // 4 - retangulo_esquerda.width // 2, 60))  # exibe a pontuação do jogador 1
    tela.blit(texto_pontuacao_direita, (LARGURA * (3 / 4) - retangulo_direita.width // 2, 60))  # exibe a pontuação do jogador 2

    # desenha todas as raquetes
    for raquete in raquetes:
        raquete.desenhar(tela)  # desenha a raquete

    # desenha a linha divisória no meio da tela
    for i in range(10, ALTURA, ALTURA // 20):
        if i % 2 == 1:
            continue  # pula uma linha para criar um efeito pontilhado
        pygame.draw.rect(tela, BRANCO, (LARGURA // 2 - 5, i, 5, ALTURA // 20))  # desenha um retângulo branco

    # desenha a bola na tela
    bola.desenhar(tela)  # desenha a bola

    # adiciona o texto do jogador
    texto_jogador1, retangulo_jogador1 = FONTE_JOGADORES.render("Jogador 1", AZUL)
    texto_jogador2, retangulo_jogador2 = FONTE_JOGADORES.render("Jogador 2", VERMELHO)
    tela.blit(texto_jogador1, (LARGURA // 4 - retangulo_jogador1.width // 2, 10))  # exibe o nome do jogador 1
    tela.blit(texto_jogador2, (LARGURA * (3 / 4) - retangulo_jogador2.width // 2, 10))  # exibe o nome do jogador 2

    if mensagem_vitoria:
        padding = 20  # define o padding desejado
        texto_vitoria, retangulo_vitoria = FONTE_VITORIA.render(mensagem_vitoria, BRANCO)
        fundo_mensagem = pygame.Surface((retangulo_vitoria.width + 2 * padding, retangulo_vitoria.height + 2 * padding))
        tela.blit(fundo_mensagem, (LARGURA // 2 - (retangulo_vitoria.width + 2 * padding) // 2, ALTURA // 2 - (retangulo_vitoria.height + 2 * padding) // 2 - 50))  # exibe o fundo da mensagem
        tela.blit(texto_vitoria, (LARGURA // 2 - retangulo_vitoria.width // 2, ALTURA // 2 - retangulo_vitoria.height // 2 - 50))  # exibe a mensagem de vitória

    if mensagem_reiniciar:
        texto_reiniciar, retangulo_reiniciar = FONTE_REINICIO.render(mensagem_reiniciar, BRANCO)
        tela.blit(texto_reiniciar, (LARGURA // 2 - retangulo_reiniciar.width // 2, ALTURA // 2 - retangulo_reiniciar.height // 2 + 50))  # exibe a mensagem de reinício

    pygame.display.update()  # atualiza a tela

def tratar_colisao(bola, raquete_esquerda, raquete_direita):
    if bola.y + bola.raio >= ALTURA:
        bola.velocidade_y *= -1  # inverte a direção da bola no eixo y ao atingir a borda inferior
    elif bola.y - bola.raio <= 0:
        bola.velocidade_y *= -1  # inverte a direção da bola no eixo y ao atingir a borda superior

    if bola.velocidade_x < 0:
        if raquete_esquerda.y <= bola.y <= raquete_esquerda.y + raquete_esquerda.altura:
            if bola.x - bola.raio <= raquete_esquerda.x + raquete_esquerda.largura:
                bola.velocidade_x *= -1  # inverte a direção da bola no eixo x ao colidir com a raquete esquerda

                # ajusta a velocidade y da bola ao colidir com a raquete
                diferenca_meio = raquete_esquerda.y + raquete_esquerda.altura / 2 - bola.y
                fator_reducao = (raquete_esquerda.altura / 2) / bola.VELOCIDADE_MAX
                bola.velocidade_y = -diferenca_meio / fator_reducao
    else:
        if raquete_direita.y <= bola.y <= raquete_direita.y + raquete_direita.altura:
            if bola.x + bola.raio >= raquete_direita.x:
                bola.velocidade_x *= -1  # inverte a direção da bola no eixo x ao colidir com a raquete direita

                # ajusta a velocidade y da bola ao colidir com a raquete
                diferenca_meio = raquete_direita.y + raquete_direita.altura / 2 - bola.y
                fator_reducao = (raquete_direita.altura / 2) / bola.VELOCIDADE_MAX
                bola.velocidade_y = -diferenca_meio / fator_reducao

def escolher_nivel(tela):
    # Configura a fonte para o menu
    FONTE_MENU = pygame.freetype.SysFont("freesansbold", 40)
    FONTE_TITULO = pygame.freetype.SysFont("freesansbold", 40)

    nivel = None
    while nivel is None:
        tela.fill(PRETO)  # Limpa a tela

        # Exibe a mensagem de boas-vindas
        texto_titulo, retangulo_titulo = FONTE_TITULO.render("Olá, seja bem-vindo(a) ao Pong!", BRANCO)
        tela.blit(texto_titulo, (LARGURA // 2 - retangulo_titulo.width // 2, ALTURA // 4 - retangulo_titulo.height // 2))

        # Desenha o menu de níveis em forma de lista
        texto_menu1, retangulo_menu1 = FONTE_MENU.render("1 - Básico", BRANCO)
        texto_menu2, retangulo_menu2 = FONTE_MENU.render("2 - Intermediário", BRANCO)
        texto_menu3, retangulo_menu3 = FONTE_MENU.render("3 - Avançado", BRANCO)

        tela.blit(texto_menu1, (LARGURA // 2 - retangulo_menu1.width // 2, ALTURA // 2 - retangulo_menu1.height // 2 - 40))
        tela.blit(texto_menu2, (LARGURA // 2 - retangulo_menu2.width // 2, ALTURA // 2 - retangulo_menu2.height // 2 + 10))
        tela.blit(texto_menu3, (LARGURA // 2 - retangulo_menu3.width // 2, ALTURA // 2 - retangulo_menu3.height // 2 + 60))

        pygame.display.update()  # Atualiza a tela

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    nivel = "básico"
                elif evento.key == pygame.K_2:
                    nivel = "intermediário"
                elif evento.key == pygame.K_3:
                    nivel = "avançado"

    return nivel


def main():
    rodando = True
    relogio = pygame.time.Clock()

    raquete_esquerda = Raquete(10, ALTURA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, AZUL)
    raquete_direita = Raquete(LARGURA - 10 - LARGURA_RAQUETE, ALTURA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, VERMELHO)
    bola = Bola(LARGURA // 2, ALTURA // 2, RAIO_BOLA)

    pontuacao_esquerda = 0
    pontuacao_direita = 0

    jogo_pausado = False
    mensagem_vitoria = None
    mensagem_reiniciar = None

    nivel = escolher_nivel(TELA)  # Passa a tela para a função de escolha de nível

    if nivel == "básico":
        Bola.VELOCIDADE_MAX = 3
        Raquete.VELOCIDADE = 5
    elif nivel == "intermediário":
        Bola.VELOCIDADE_MAX = 7
        Raquete.VELOCIDADE = 9
    elif nivel == "avançado":
        Bola.VELOCIDADE_MAX = 20
        Raquete.VELOCIDADE = 10

    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                break

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r and jogo_pausado:
                    pontuacao_esquerda = 0
                    pontuacao_direita = 0
                    bola.resetar()
                    raquete_esquerda.resetar()
                    raquete_direita.resetar()
                    jogo_pausado = False
                    mensagem_vitoria = None
                    mensagem_reiniciar = None

        if not jogo_pausado:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w] and raquete_esquerda.y - raquete_esquerda.VELOCIDADE >= 0:
                raquete_esquerda.mover(cima=True)
            if keys[pygame.K_s] and raquete_esquerda.y + raquete_esquerda.altura + raquete_esquerda.VELOCIDADE <= ALTURA:
                raquete_esquerda.mover(cima=False)
            if keys[pygame.K_UP] and raquete_direita.y - raquete_direita.VELOCIDADE >= 0:
                raquete_direita.mover(cima=True)
            if keys[pygame.K_DOWN] and raquete_direita.y + raquete_direita.altura + raquete_direita.VELOCIDADE <= ALTURA:
                raquete_direita.mover(cima=False)

            bola.mover()
            tratar_colisao(bola, raquete_esquerda, raquete_direita)

            if bola.x < 0:
                pontuacao_direita += 1
                bola.resetar()
            elif bola.x > LARGURA:
                pontuacao_esquerda += 1
                bola.resetar()

            if pontuacao_esquerda >= PONTUACAO_VITORIA:
                mensagem_vitoria = "Jogador 1 ganhou!"
                mensagem_reiniciar = "Press 'R' para recomeçar"
                jogo_pausado = True
            elif pontuacao_direita >= PONTUACAO_VITORIA:
                mensagem_vitoria = "Jogador 2 ganhou!"
                mensagem_reiniciar = "Pressione 'R' para recomeçar"
                jogo_pausado = True

        desenhar(TELA, [raquete_esquerda, raquete_direita], bola, pontuacao_esquerda, pontuacao_direita, mensagem_reiniciar, mensagem_vitoria)

    pygame.quit()

if __name__ == "__main__":
    main()
