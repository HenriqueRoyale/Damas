import os
import platform
import time


def limparTela():
    """Limpa a tela do terminal"""
    sistema = platform.system()
    if sistema == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


class Movimento:
    def __init__(self, linOrig=0, colOrig=0, linDest=0, colDest=0):
        self.linOrig = linOrig
        self.colOrig = colOrig
        self.linDest = linDest
        self.colDest = colDest


def montarTabuleiro(tabuleiro):
    n = 2
    # Montando as peças Brancas
    for lin in range(0, 3):
        for col in range(0, 8):
            if (lin + col) % 2 != 0:
                tabuleiro[lin][col] = n
                n += 2
            else:
                tabuleiro[lin][col] = -1
    
    # Montando as peças Pretas
    n = 23
    for lin in range(5, 8):
        for col in range(0, 8):
            if (lin + col) % 2 != 0:
                tabuleiro[lin][col] = n
                n -= 2
            else:
                tabuleiro[lin][col] = -1
    
    for lin in range(3, 5):
        for col in range(0, 8):
            if (lin + col) % 2 != 0:
                tabuleiro[lin][col] = 0
            else:
                tabuleiro[lin][col] = -1


def mostrarTabuleiro(tabuleiro):
    for lin in range(0, 8):
        # Imprime o número da linha (1-8) no lado esquerdo
        print(f"{lin + 1} ", end="")
        
        for col in range(0, 8):
            if tabuleiro[lin][col] == -1:
                # Casa inválida (não jogável)
                print("| ", end="")
            elif tabuleiro[lin][col] == 0:
                # Casa vazia
                print("| ", end="")
            elif tabuleiro[lin][col] % 2 == 0:
                # Peça BRANCA (números pares: 2, 4, 6, ...)
                if ehDama(tabuleiro[lin][col]):
                    print("|◉", end="")  # Dama branca
                else:
                    print("|○", end="")  # Peça branca normal
            else:
                # Peça PRETA (números ímpares: 23, 21, 19, ...)
                if ehDama(tabuleiro[lin][col]):
                    print("|◉", end="")  # Dama preta
                else:
                    print("|●", end="")  # Peça preta normal
            print("|", end="")
        print()
    
    # Imprime as letras das colunas (A-H) abaixo do tabuleiro
    print("  ", end="")
    for col in range(0, 8):
        print(f" {chr(ord('a') + col)} ", end="")
    print()


def verificaMovimento(tabuleiro, peca, Destino):
    confirmacao = 0
    lin_peca = 0
    col_peca = 0
    lin_destino = 0
    col_destino = 0
    
    for i in range(0, 8):
        for j in range(0, 8):
            if tabuleiro[i][j] == peca:
                lin_peca = i
                col_peca = j
                confirmacao += 1
            if tabuleiro[i][j] == Destino:
                lin_destino = i
                col_destino = j
                confirmacao += 1
            if confirmacao < 2:
                return 1
            else:
                return 0
    return 0


def posicaoValida(lin, col):
    # Verifica se a posição está dentro dos limites do tabuleiro (0-7)
    return (lin >= 0 and lin <= 7 and col >= 0 and col <= 7)


def sequenciaCaptura(tabuleiro, lin_peca, col_peca, direcao, cont_pecas_comidas):
    peca_atual = tabuleiro[lin_peca][col_peca]
    eh_dama = ehDama(peca_atual)
    
    # Direita cima
    if (direcao == -1 or eh_dama) and posicaoValida(lin_peca - 1, col_peca + 1) and posicaoValida(lin_peca - 2, col_peca + 2):
        meio = tabuleiro[lin_peca - 1][col_peca + 1]
        destino = tabuleiro[lin_peca - 2][col_peca + 2]
        # Verifica se tem inimigo na casa do meio e se a casa de destino está vazia
        if meio > 0 and (meio % 2 != peca_atual % 2) and destino == 0:
            tabuleiro[lin_peca - 2][col_peca + 2] = peca_atual
            tabuleiro[lin_peca][col_peca] = 0  # Limpa a posição atual
            tabuleiro[lin_peca - 1][col_peca + 1] = 0
            cont_pecas_comidas[0] += 1
            coroarPeca(tabuleiro, lin_peca - 2, col_peca + 2)
            sequenciaCaptura(tabuleiro, lin_peca - 2, col_peca + 2, direcao, cont_pecas_comidas)
            return
    
    # Direita baixo
    if (direcao == 1 or eh_dama) and posicaoValida(lin_peca + 1, col_peca + 1) and posicaoValida(lin_peca + 2, col_peca + 2):
        meio = tabuleiro[lin_peca + 1][col_peca + 1]
        destino = tabuleiro[lin_peca + 2][col_peca + 2]
        if meio > 0 and (meio % 2 != peca_atual % 2) and destino == 0:
            tabuleiro[lin_peca + 2][col_peca + 2] = peca_atual
            tabuleiro[lin_peca][col_peca] = 0  # Limpa a posição atual
            tabuleiro[lin_peca + 1][col_peca + 1] = 0
            cont_pecas_comidas[0] += 1
            coroarPeca(tabuleiro, lin_peca + 2, col_peca + 2)
            sequenciaCaptura(tabuleiro, lin_peca + 2, col_peca + 2, direcao, cont_pecas_comidas)
            return
    
    # Esquerda cima
    if (direcao == -1 or eh_dama) and posicaoValida(lin_peca - 1, col_peca - 1) and posicaoValida(lin_peca - 2, col_peca - 2):
        meio = tabuleiro[lin_peca - 1][col_peca - 1]
        destino = tabuleiro[lin_peca - 2][col_peca - 2]
        if meio > 0 and (meio % 2 != peca_atual % 2) and destino == 0:
            tabuleiro[lin_peca - 2][col_peca - 2] = peca_atual
            tabuleiro[lin_peca][col_peca] = 0  # Limpa a posição atual
            tabuleiro[lin_peca - 1][col_peca - 1] = 0
            cont_pecas_comidas[0] += 1
            coroarPeca(tabuleiro, lin_peca - 2, col_peca - 2)
            sequenciaCaptura(tabuleiro, lin_peca - 2, col_peca - 2, direcao, cont_pecas_comidas)
            return
    
    # Esquerda baixo
    if (direcao == 1 or eh_dama) and posicaoValida(lin_peca + 1, col_peca - 1) and posicaoValida(lin_peca + 2, col_peca - 2):
        meio = tabuleiro[lin_peca + 1][col_peca - 1]
        destino = tabuleiro[lin_peca + 2][col_peca - 2]
        if meio > 0 and (meio % 2 != peca_atual % 2) and destino == 0:
            tabuleiro[lin_peca + 2][col_peca - 2] = peca_atual
            tabuleiro[lin_peca][col_peca] = 0  # Limpa a posição atual
            tabuleiro[lin_peca + 1][col_peca - 1] = 0
            cont_pecas_comidas[0] += 1
            coroarPeca(tabuleiro, lin_peca + 2, col_peca - 2)
            sequenciaCaptura(tabuleiro, lin_peca + 2, col_peca - 2, direcao, cont_pecas_comidas)
            return


def coroarPeca(tabuleiro, lin, col):
    """Coroa uma peça quando ela chega ao final do tabuleiro"""
    if tabuleiro[lin][col] > 0:
        # Pretas (ímpares) chegam na linha 0, Brancas (pares) chegam na linha 7
        if tabuleiro[lin][col] % 2 != 0 and lin == 0:  # Preta chegou ao topo
            # Marca como dama adicionando 100 (mantém paridade)
            tabuleiro[lin][col] += 100
            return True
        elif tabuleiro[lin][col] % 2 == 0 and lin == 7:  # Branca chegou ao fundo
            # Marca como dama adicionando 100 (mantém paridade)
            tabuleiro[lin][col] += 100
            return True
    return False


def ehDama(peca):
    """Verifica se uma peça é uma dama"""
    return peca > 100


def aplicaMovimento(tabuleiro, lin_peca_idx, col_peca_idx, lin_Destino_idx, col_Destino_idx, direcao, cont_pretas, cont_brancas):
    cont_pecas_capturadas = [0]
    dlin = lin_Destino_idx - lin_peca_idx
    dcol = abs(col_Destino_idx - col_peca_idx)
    peca_original = tabuleiro[lin_peca_idx][col_peca_idx]
    eh_dama = ehDama(peca_original)

    # Verifica se é uma captura (movimento de 2 casas na diagonal)
    if abs(dlin) == 2 and dcol == 2:
        # Calcula a posição da peça capturada (meio do caminho)
        lin_capturada = (lin_peca_idx + lin_Destino_idx) // 2
        col_capturada = (col_peca_idx + col_Destino_idx) // 2
        
        # Verifica se há uma peça inimiga na posição intermediária
        if posicaoValida(lin_capturada, col_capturada):
            peca_meio = tabuleiro[lin_capturada][col_capturada]
            if peca_meio > 0 and (peca_meio % 2 != peca_original % 2):  # É uma peça inimiga
                # Move a peça para o destino
                tabuleiro[lin_Destino_idx][col_Destino_idx] = peca_original
                tabuleiro[lin_peca_idx][col_peca_idx] = 0  # Limpa a posição original
                tabuleiro[lin_capturada][col_capturada] = 0  # Remove a peça capturada
                cont_pecas_capturadas[0] = 1  # Conta a primeira peça capturada
                # Verifica sequência de capturas
                sequenciaCaptura(tabuleiro, lin_Destino_idx, col_Destino_idx, direcao, cont_pecas_capturadas)
            else:
                # Não há peça inimiga, movimento inválido
                return
        else:
            # Posição intermediária inválida
            return
    elif abs(dlin) == 1 and dcol == 1:
        # Movimento simples de 1 casa
        if not eh_dama and dlin != direcao:
            # Peça normal só pode se mover na direção correta
            return
        tabuleiro[lin_Destino_idx][col_Destino_idx] = peca_original
        tabuleiro[lin_peca_idx][col_peca_idx] = 0
    else:
        # Movimento inválido
        return

    # Coroa a peça se chegou ao final do tabuleiro
    coroarPeca(tabuleiro, lin_Destino_idx, col_Destino_idx)

    if cont_pecas_capturadas[0] > 0:
        if direcao == -1 and cont_brancas is not None:
            cont_brancas[0] -= cont_pecas_capturadas[0]
        if direcao == 1 and cont_pretas is not None:
            cont_pretas[0] -= cont_pecas_capturadas[0]


def copia_tabuleiro(origem, destino):
    for i in range(0, 8):
        for j in range(0, 8):
            destino[i][j] = origem[i][j]


def contarPecas(tabuleiro, cont_pretas, cont_brancas):
    p = 0
    b = 0
    for lin in range(0, 8):
        for col in range(0, 8):
            if tabuleiro[lin][col] > 0:
                if tabuleiro[lin][col] % 2 == 0:
                    b += 1
                else:
                    p += 1
    cont_pretas[0] = p
    cont_brancas[0] = b


# Calcula a força estratégica do tabuleiro
# Avalia a qualidade de cada peça (proteção, posição, etc.)
# Retorna diferença de força: positivo = bom para brancas, negativo = bom para pretas
def calcularForcaTabuleiro(tabuleiro):
    forca_brancas = 0
    forca_pretas = 0
    
    for lin in range(0, 8):
        for col in range(0, 8):
            if tabuleiro[lin][col] > 0:
                forca_peca = 0
                
                # 1. Força base da peça
                forca_peca = 10
                
                # 2. Bônus se peça está protegida (tem peça aliada atrás)
                if tabuleiro[lin][col] % 2 == 0:  # Branca
                    if posicaoValida(lin + 1, col - 1) and tabuleiro[lin + 1][col - 1] > 0 and tabuleiro[lin + 1][col - 1] % 2 == 0:
                        forca_peca += 2  # Protegida por trás esquerda
                    if posicaoValida(lin + 1, col + 1) and tabuleiro[lin + 1][col + 1] > 0 and tabuleiro[lin + 1][col + 1] % 2 == 0:
                        forca_peca += 2  # Protegida por trás direita
                else:  # Preta
                    if posicaoValida(lin - 1, col - 1) and tabuleiro[lin - 1][col - 1] > 0 and tabuleiro[lin - 1][col - 1] % 2 != 0:
                        forca_peca += 2
                    if posicaoValida(lin - 1, col + 1) and tabuleiro[lin - 1][col + 1] > 0 and tabuleiro[lin - 1][col + 1] % 2 != 0:
                        forca_peca += 2
                
                # 3. Bônus se está na última linha (proteção)
                if tabuleiro[lin][col] % 2 == 0 and lin == 7:  # Branca na última linha
                    forca_peca += 3
                if tabuleiro[lin][col] % 2 != 0 and lin == 0:  # Preta na última linha
                    forca_peca += 3
                
                # 4. Adiciona à força total
                if tabuleiro[lin][col] % 2 == 0:
                    forca_brancas += forca_peca
                else:
                    forca_pretas += forca_peca
    
    return forca_brancas - forca_pretas  # Diferença de força


# Função de avaliação posicional do tabuleiro
# Retorna score positivo = bom para brancas, negativo = bom para pretas
def avaliarTabuleiro(tabuleiro):
    score = 0
    cont_brancas = 0
    cont_pretas = 0
    brancas_avancadas = 0
    pretas_avancadas = 0
    brancas_centro = 0
    pretas_centro = 0
    
    for lin in range(0, 8):
        for col in range(0, 8):
            if tabuleiro[lin][col] > 0:
                if tabuleiro[lin][col] % 2 == 0:  # Peça branca (par)
                    cont_brancas += 1
                    
                    # Bônus posicional: peças mais avançadas (linhas 4-7) valem mais
                    if lin >= 4:
                        brancas_avancadas += 1
                    
                    # Bônus de controle do centro (colunas 2-5)
                    if col >= 2 and col <= 5:
                        brancas_centro += 1
                else:  # Peça preta (ímpar)
                    cont_pretas += 1
                    
                    # Bônus posicional: peças mais avançadas (linhas 0-3) valem mais
                    if lin <= 3:
                        pretas_avancadas += 1
                    
                    # Bônus de controle do centro
                    if col >= 2 and col <= 5:
                        pretas_centro += 1
    
    # Score baseado em material (diferença de peças)
    score = (cont_brancas - cont_pretas) * 10
    
    # Bônus posicional: peças avançadas valem mais
    score += brancas_avancadas * 2
    score -= pretas_avancadas * 2
    
    # Bônus de controle do centro
    score += brancas_centro
    score -= pretas_centro
    
    # Adiciona a força estratégica do tabuleiro (peças protegidas, posição, etc.)
    score += calcularForcaTabuleiro(tabuleiro)
    
    return score


# Gera todos os movimentos possíveis dinamicamente
# Retorna a quantidade de movimentos encontrados e a lista de movimentos
def geraMovimentos(tabuleiro, direcao):
    lista = []
    
    for lin in range(0, 8):
        for col in range(0, 8):
            peca = tabuleiro[lin][col]
            if peca <= 0:
                continue
            
            eh_dama = ehDama(peca)
            
            if direcao == -1:  # Pretas
                if peca % 2 != 0:  # é uma peça preta (ímpar)
                    # direita cima
                    if posicaoValida(lin - 1, col + 1) and tabuleiro[lin - 1][col + 1] > 0 and tabuleiro[lin - 1][col + 1] % 2 == 0:  # peça inimiga no caminho
                        if posicaoValida(lin - 2, col + 2) and tabuleiro[lin - 2][col + 2] == 0:  # destino vazio
                            mov = Movimento(lin, col, lin - 2, col + 2)
                            lista.append(mov)
                    elif posicaoValida(lin - 1, col + 1) and tabuleiro[lin - 1][col + 1] == 0:  # não tem nada no caminho
                        mov = Movimento(lin, col, lin - 1, col + 1)
                        lista.append(mov)
                    
                    # esquerda cima
                    if posicaoValida(lin - 1, col - 1) and tabuleiro[lin - 1][col - 1] > 0 and tabuleiro[lin - 1][col - 1] % 2 == 0:  # peça inimiga no caminho
                        if posicaoValida(lin - 2, col - 2) and tabuleiro[lin - 2][col - 2] == 0:  # destino vazio
                            mov = Movimento(lin, col, lin - 2, col - 2)
                            lista.append(mov)
                    elif posicaoValida(lin - 1, col - 1) and tabuleiro[lin - 1][col - 1] == 0:  # Não tem nada no caminho
                        mov = Movimento(lin, col, lin - 1, col - 1)
                        lista.append(mov)
                    
                    # Se for dama, também pode mover para baixo
                    if eh_dama:
                        # direita baixo
                        if posicaoValida(lin + 1, col + 1) and tabuleiro[lin + 1][col + 1] > 0 and tabuleiro[lin + 1][col + 1] % 2 == 0:
                            if posicaoValida(lin + 2, col + 2) and tabuleiro[lin + 2][col + 2] == 0:
                                mov = Movimento(lin, col, lin + 2, col + 2)
                                lista.append(mov)
                        elif posicaoValida(lin + 1, col + 1) and tabuleiro[lin + 1][col + 1] == 0:
                            mov = Movimento(lin, col, lin + 1, col + 1)
                            lista.append(mov)
                        
                        # esquerda baixo
                        if posicaoValida(lin + 1, col - 1) and tabuleiro[lin + 1][col - 1] > 0 and tabuleiro[lin + 1][col - 1] % 2 == 0:
                            if posicaoValida(lin + 2, col - 2) and tabuleiro[lin + 2][col - 2] == 0:
                                mov = Movimento(lin, col, lin + 2, col - 2)
                                lista.append(mov)
                        elif posicaoValida(lin + 1, col - 1) and tabuleiro[lin + 1][col - 1] == 0:
                            mov = Movimento(lin, col, lin + 1, col - 1)
                            lista.append(mov)
            
            if direcao == 1:  # Brancas
                if peca % 2 == 0:  # é uma peça branca (par)
                    # direita baixo
                    if posicaoValida(lin + 1, col + 1) and tabuleiro[lin + 1][col + 1] > 0 and tabuleiro[lin + 1][col + 1] % 2 != 0:  # peça inimiga no caminho
                        if posicaoValida(lin + 2, col + 2) and tabuleiro[lin + 2][col + 2] == 0:  # destino vazio
                            mov = Movimento(lin, col, lin + 2, col + 2)
                            lista.append(mov)
                    elif posicaoValida(lin + 1, col + 1) and tabuleiro[lin + 1][col + 1] == 0:  # não tem nada no caminho
                        mov = Movimento(lin, col, lin + 1, col + 1)
                        lista.append(mov)
                    
                    # esquerda baixo
                    if posicaoValida(lin + 1, col - 1) and tabuleiro[lin + 1][col - 1] > 0 and tabuleiro[lin + 1][col - 1] % 2 != 0:  # peça inimiga no caminho
                        if posicaoValida(lin + 2, col - 2) and tabuleiro[lin + 2][col - 2] == 0:  # destino vazio
                            mov = Movimento(lin, col, lin + 2, col - 2)
                            lista.append(mov)
                    elif posicaoValida(lin + 1, col - 1) and tabuleiro[lin + 1][col - 1] == 0:  # Não tem nada no caminho
                        mov = Movimento(lin, col, lin + 1, col - 1)
                        lista.append(mov)
                    
                    # Se for dama, também pode mover para cima
                    if eh_dama:
                        # direita cima
                        if posicaoValida(lin - 1, col + 1) and tabuleiro[lin - 1][col + 1] > 0 and tabuleiro[lin - 1][col + 1] % 2 != 0:
                            if posicaoValida(lin - 2, col + 2) and tabuleiro[lin - 2][col + 2] == 0:
                                mov = Movimento(lin, col, lin - 2, col + 2)
                                lista.append(mov)
                        elif posicaoValida(lin - 1, col + 1) and tabuleiro[lin - 1][col + 1] == 0:
                            mov = Movimento(lin, col, lin - 1, col + 1)
                            lista.append(mov)
                        
                        # esquerda cima
                        if posicaoValida(lin - 1, col - 1) and tabuleiro[lin - 1][col - 1] > 0 and tabuleiro[lin - 1][col - 1] % 2 != 0:
                            if posicaoValida(lin - 2, col - 2) and tabuleiro[lin - 2][col - 2] == 0:
                                mov = Movimento(lin, col, lin - 2, col - 2)
                                lista.append(mov)
                        elif posicaoValida(lin - 1, col - 1) and tabuleiro[lin - 1][col - 1] == 0:
                            mov = Movimento(lin, col, lin - 1, col - 1)
                            lista.append(mov)
    
    return lista


def minimax(tabuleiro, profundidade, profundidadeMax, maximizando, direcao):
    if profundidade == profundidadeMax:
        return avaliarTabuleiro(tabuleiro)
    
    if maximizando:
        direcao = 1
        alfa = -99999
        movimentos = geraMovimentos(tabuleiro, direcao)
        
        if len(movimentos) == 0:
            return avaliarTabuleiro(tabuleiro)
        
        for i in range(0, len(movimentos)):
            tabuleiro_temp = [[0 for _ in range(8)] for _ in range(8)]
            copia_tabuleiro(tabuleiro, tabuleiro_temp)
            aplicaMovimento(tabuleiro_temp, movimentos[i].linOrig, movimentos[i].colOrig, movimentos[i].linDest, movimentos[i].colDest, direcao, None, None)
            score = minimax(tabuleiro_temp, profundidade + 1, profundidadeMax, 0, direcao)
            if score > alfa:
                alfa = score
        
        return alfa
    else:
        direcao = -1
        beta = 99999
        movimentos = geraMovimentos(tabuleiro, direcao)
        
        if len(movimentos) == 0:
            return avaliarTabuleiro(tabuleiro)
        
        for i in range(0, len(movimentos)):
            tabuleiro_temp = [[0 for _ in range(8)] for _ in range(8)]
            copia_tabuleiro(tabuleiro, tabuleiro_temp)
            aplicaMovimento(tabuleiro_temp, movimentos[i].linOrig, movimentos[i].colOrig, movimentos[i].linDest, movimentos[i].colDest, direcao, None, None)
            score = minimax(tabuleiro_temp, profundidade + 1, profundidadeMax, 1, direcao)
            if score < beta:
                beta = score
        
        return beta

def temCapturasPossiveis(tabuleiro, direcao):
    """Verifica se há capturas possíveis para o jogador"""
    movimentos = geraMovimentos(tabuleiro, direcao)
    for mov in movimentos:
        dlin = mov.linDest - mov.linOrig
        dcol = abs(mov.colDest - mov.colOrig)
        if abs(dlin) == 2 and dcol == 2:  # É uma captura
            return True
    return False


def main():
    tabuleiro = [[0 for _ in range(8)] for _ in range(8)]
    cont_pretas = [12]
    cont_brancas = [12]
    vez_jogador = 1  # 1 = jogador (pretas), 0 = IA (brancas)
    
    # Montando o Tabuleiro de Dama
    montarTabuleiro(tabuleiro)
    
    limparTela()
    print("=== JOGO DE DAMAS ===")
    print("Você joga com as peças PRETAS (●)")
    print("A IA joga com as peças BRANCAS (○)")
    print("Damas são representadas por ◉")
    print()
    
    while cont_pretas[0] > 0 and cont_brancas[0] > 0:
        # Recalcula contagens a partir do tabuleiro para evitar dessincronia
        contarPecas(tabuleiro, cont_pretas, cont_brancas)
        if cont_pretas[0] <= 0 or cont_brancas[0] <= 0:
            break
        
        # Limpa a tela antes de mostrar o tabuleiro
        limparTela()
        
        # Mostrando o Tabuleiro
        print("=== JOGO DE DAMAS ===")
        print(f"Peças Pretas: {cont_pretas[0]} | Peças Brancas: {cont_brancas[0]}")
        mostrarTabuleiro(tabuleiro)
        
        if vez_jogador:
            # ======== VEZ DO JOGADOR (PRETAS) ========
            direcao = -1
            
            # Verifica se há capturas obrigatórias
            tem_capturas = temCapturasPossiveis(tabuleiro, direcao)
            if tem_capturas:
                print("⚠️  ATENÇÃO: Você tem capturas obrigatórias!")
            
            # ========
            # Peça
            # ========
            flag = True
            col_peca_idx = 0
            lin_peca_idx = 0
            
            while flag:
                try:
                    entrada = input("\nDigite a Peça que deseja mover (ex: E 3): ").strip().split()
                    if len(entrada) != 2:
                        print("Entrada inválida para a peça. Tente novamente.")
                        continue
                    
                    colunaPeca = entrada[0].lower()
                    linhaPeca = int(entrada[1])
                    
                    col_peca_idx = ord(colunaPeca) - ord('a')
                    lin_peca_idx = linhaPeca - 1
                    
                    if not posicaoValida(lin_peca_idx, col_peca_idx):
                        print("Casa da peça fora do tabuleiro. Tente novamente.")
                        continue
                    
                    peca = tabuleiro[lin_peca_idx][col_peca_idx]
                    if peca <= 0:
                        print("Não há peça nessa casa. Tente novamente.")
                        continue
                    # Jogador joga com pretas (ímpares)
                    if peca % 2 == 0:
                        print("Essa peça não é sua (você joga com pretas). Tente novamente.")
                        continue
                    
                    flag = False  # Todas as validações passaram
                except (ValueError, IndexError):
                    print("Entrada inválida para a peça. Tente novamente.")
                    continue
            
            # ========
            # Destino
            # ========
            flag = True
            col_Destino_idx = 0
            lin_Destino_idx = 0
            
            while flag:
                try:
                    entrada = input("Digite para onde quer mover a peça (ex: E 7): ").strip().split()
                    if len(entrada) != 2:
                        print("Entrada inválida para destino. Tente novamente.")
                        continue
                    
                    colunaDestino = entrada[0].lower()
                    linhaDestino = int(entrada[1])
                    
                    # Converte letra para índice de coluna (A-H -> 0-7) e linha para 0-7
                    col_Destino_idx = ord(colunaDestino) - ord('a')
                    lin_Destino_idx = linhaDestino - 1
                    
                    if not posicaoValida(lin_Destino_idx, col_Destino_idx):
                        print("Destino fora do tabuleiro. Tente novamente.")
                        continue
                    
                    Destino = tabuleiro[lin_Destino_idx][col_Destino_idx]
                    if Destino < 0:
                        print("Destino inválido (casa não jogável). Tente novamente.")
                        continue
                    if Destino != 0:
                        print("O destino deve estar vazio. Tente novamente.")
                        continue
                    
                    # Valida movimento: diagonal 1 casa (simples) ou 2 (captura)
                    dlin = lin_Destino_idx - lin_peca_idx
                    dcol = abs(col_Destino_idx - col_peca_idx)
                    movimento_valido = False
                    peca_atual = tabuleiro[lin_peca_idx][col_peca_idx]
                    eh_dama = ehDama(peca_atual)
                    
                    if eh_dama:
                        # Damas podem se mover qualquer distância diagonal
                        if abs(dlin) == abs(dcol) and abs(dlin) >= 1:
                            movimento_valido = True
                    else:
                        # Peças normais: 1 casa ou 2 casas (captura)
                        if dlin == -1 and dcol == 1:
                            movimento_valido = True
                        if dlin == -2 and dcol == 2:
                            # Verifica se há uma peça inimiga para capturar
                            lin_meio = (lin_peca_idx + lin_Destino_idx) // 2
                            col_meio = (col_peca_idx + col_Destino_idx) // 2
                            if posicaoValida(lin_meio, col_meio):
                                peca_meio = tabuleiro[lin_meio][col_meio]
                                if peca_meio > 0 and (peca_meio % 2 != peca_atual % 2):
                                    movimento_valido = True
                                else:
                                    print("Não há peça inimiga para capturar nessa posição.")
                                    continue
                            else:
                                movimento_valido = False
                    
                    if not movimento_valido:
                        print("Movimento inválido. Tente novamente.")
                        continue
                    
                    # Se há capturas obrigatórias, só permite capturas
                    if tem_capturas and abs(dlin) != 2:
                        print("Você deve fazer uma captura! Tente novamente.")
                        continue
                    
                    flag = False  # Todas as validações passaram
                except (ValueError, IndexError):
                    print("Entrada inválida para destino. Tente novamente.")
                    continue
            
            # Fazendo o movimento do jogador (pretas)
            aplicaMovimento(tabuleiro, lin_peca_idx, col_peca_idx, lin_Destino_idx, col_Destino_idx, direcao, cont_pretas, cont_brancas)
            vez_jogador = 0
        else:
            # ======== VEZ DA IA (BRANCAS) ========
            direcao = 1
            
            
            # Simula pensamento com pontos animados
            for _ in range(3):
                time.sleep(0.5)
                print(".", end="", flush=True)
            print()
            
            movimentos_ia = geraMovimentos(tabuleiro, direcao)
            
            if len(movimentos_ia) == 0:
                print("IA sem movimentos.")
                vez_jogador = 1
            else:
                # Verifica se há capturas obrigatórias
                tem_capturas = temCapturasPossiveis(tabuleiro, direcao)
                
                # Se há capturas obrigatórias, filtra apenas movimentos de captura
                if tem_capturas:
                    movimentos_captura = []
                    for mov in movimentos_ia:
                        dlin = abs(mov.linDest - mov.linOrig)
                        dcol = abs(mov.colDest - mov.colOrig)
                        if dlin == 2 and dcol == 2:  # É uma captura
                            movimentos_captura.append(mov)
                    
                    if len(movimentos_captura) > 0:
                        movimentos_ia = movimentos_captura
                
                melhor_idx = 0
                melhor_score = -99999
                profundidadeMax = 4
                
                # Simula processamento de cada movimento
                
                for i in range(0, len(movimentos_ia)):
                    
                    
                    
                    tab_temp = [[0 for _ in range(8)] for _ in range(8)]
                    copia_tabuleiro(tabuleiro, tab_temp)
                    aplicaMovimento(tab_temp, movimentos_ia[i].linOrig, movimentos_ia[i].colOrig, movimentos_ia[i].linDest, movimentos_ia[i].colDest, direcao, None, None)
                    s = minimax(tab_temp, 1, profundidadeMax, 0, -1)
                    if s > melhor_score:
                        melhor_score = s
                        melhor_idx = i
                
                print()  # Nova linha após os pontos
                
                
                mov_escolhido = movimentos_ia[melhor_idx]
                origem_col = chr(ord('a') + mov_escolhido.colOrig)
                origem_lin = mov_escolhido.linOrig + 1
                dest_col = chr(ord('a') + mov_escolhido.colDest)
                dest_lin = mov_escolhido.linDest + 1
               
                
                time.sleep(1)  # Delay antes de aplicar o movimento e limpar a tela
                
                aplicaMovimento(tabuleiro, mov_escolhido.linOrig, mov_escolhido.colOrig, mov_escolhido.linDest, mov_escolhido.colDest, direcao, cont_pretas, cont_brancas)
                vez_jogador = 1
                # Limpa a tela após o movimento da IA
                limparTela()
    
    print("\n" + "="*30)
    if cont_brancas[0] == 0:
        print("🎉 PARABÉNS! Pretas venceram!")
    else:
        print("🤖 IA venceu! Brancas venceram!")
    print("="*30)


if __name__ == "__main__":
    main()



