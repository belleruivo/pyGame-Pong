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
VERDE = (0, 128, 0)  # cor verde mais escura e sutil para o fundo da mensagem de vitória
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
        fundo_mensagem.fill(VERDE)  # preenche o fundo da mensagem com a cor verde
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

def main():
    rodando = True  # variável que controla o loop principal do jogo
    relogio = pygame.time.Clock()  # cria um objeto para controlar o tempo de atualização do jogo

    raquete_esquerda = Raquete(10, ALTURA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, AZUL)  # cria a raquete esquerda
    raquete_direita = Raquete(LARGURA - 10 - LARGURA_RAQUETE, ALTURA // 2 - ALTURA_RAQUETE // 2, LARGURA_RAQUETE, ALTURA_RAQUETE, VERMELHO)  # cria a raquete direita
    bola = Bola(LARGURA // 2, ALTURA // 2, RAIO_BOLA)  # cria a bola

    pontuacao_esquerda = 0  # inicializa a pontuação do jogador 1
    pontuacao_direita = 0  # inicializa a pontuação do jogador 2

    jogo_pausado = False  # variável para controlar se o jogo está pausado
    mensagem_vitoria = None  # mensagem de vitória a ser exibida
    mensagem_reiniciar = None  # mensagem de reinício a ser exibida

    while rodando:
        relogio.tick(FPS)  # controla a taxa de atualização do jogo

        for evento in pygame.event.get():  # loop para capturar eventos do jogo
            if evento.type == pygame.QUIT:  # evento de fechar a janela do jogo
                rodando = False  # encerra o loop principal
                break

            if evento.type == pygame.KEYDOWN:  # evento de pressionar uma tecla
                if evento.key == pygame.K_r and jogo_pausado:  # se a tecla 'R' for pressionada e o jogo estiver pausado
                    pontuacao_esquerda = 0  # reseta a pontuação do jogador 1
                    pontuacao_direita = 0  # reseta a pontuação do jogador 2
                    bola.resetar()  # reseta a posição e a velocidade da bola
                    raquete_esquerda.resetar()  # reseta a posição da raquete esquerda
                    raquete_direita.resetar()  # reseta a posição da raquete direita
                    jogo_pausado = False  # despausa o jogo
                    mensagem_vitoria = None  # reseta a mensagem de vitória
                    mensagem_reiniciar = None  # reseta a mensagem de reinício

        if not jogo_pausado:  # se o jogo não estiver pausado, atualiza o estado do jogo
            keys = pygame.key.get_pressed()  # captura as teclas pressionadas

            # movimentação das raquetes
            if keys[pygame.K_w] and raquete_esquerda.y - raquete_esquerda.VELOCIDADE >= 0:  # movimenta a raquete esquerda para cima
                raquete_esquerda.mover(cima=True)
            if keys[pygame.K_s] and raquete_esquerda.y + raquete_esquerda.altura + raquete_esquerda.VELOCIDADE <= ALTURA:  # movimenta a raquete esquerda para baixo
                raquete_esquerda.mover(cima=False)
            if keys[pygame.K_UP] and raquete_direita.y - raquete_direita.VELOCIDADE >= 0:  # movimenta a raquete direita para cima
                raquete_direita.mover(cima=True)
            if keys[pygame.K_DOWN] and raquete_direita.y + raquete_direita.altura + raquete_direita.VELOCIDADE <= ALTURA:  # movimenta a raquete direita para baixo
                raquete_direita.mover(cima=False)

            bola.mover()  # move a bola

            tratar_colisao(bola, raquete_esquerda, raquete_direita)  # trata as colisões da bola com as raquetes e as bordas da tela

            # atualiza a pontuação e reseta a bola se ela sair da tela
            if bola.x < 0:
                pontuacao_direita += 1  # incrementa a pontuação do jogador 2
                bola.resetar()  # reseta a bola
            elif bola.x > LARGURA:
                pontuacao_esquerda += 1  # incrementa a pontuação do jogador 1
                bola.resetar()  # reseta a bola

            # verifica se algum jogador venceu o jogo
            if pontuacao_esquerda >= PONTUACAO_VITORIA:
                mensagem_vitoria = "Jogador 1 ganhou!"
                mensagem_reiniciar = "Press 'R' para recomeçar"
                jogo_pausado = True  # pausa o jogo
            elif pontuacao_direita >= PONTUACAO_VITORIA:
                mensagem_vitoria = "Jogador 2 ganhou!"
                mensagem_reiniciar = "Pressione 'R' para recomeçar"
                jogo_pausado = True  # pausa o jogo

        desenhar(TELA, [raquete_esquerda, raquete_direita], bola, pontuacao_esquerda, pontuacao_direita, mensagem_reiniciar, mensagem_vitoria)  # desenha os elementos do jogo na tela

    pygame.quit()  # encerra o pygame

if __name__ == "__main__":
    main()  # inicia o jogo
