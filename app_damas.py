import streamlit as st
import time

# ==========================================
# 1. LÓGICA ORIGINAL DO JOGO (INTACTA)
# ==========================================

class Movimento:
    def __init__(self, linOrig=0, colOrig=0, linDest=0, colDest=0):
        self.linOrig = linOrig
        self.colOrig = colOrig
        self.linDest = linDest
        self.colDest = colDest

def montarTabuleiro(tabuleiro):
    n = 2
    for lin in range(0, 3):
        for col in range(0, 8):
            if (lin + col) % 2 != 0:
                tabuleiro[lin][col] = n
                n += 2
            else:
                tabuleiro[lin][col] = -1
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

def posicaoValida(lin, col):
    return (lin >= 0 and lin <= 7 and col >= 0 and col <= 7)

def ehDama(peca):
    return peca > 100

def coroarPeca(tabuleiro, lin, col):
    if tabuleiro[lin][col] > 0:
        if tabuleiro[lin][col] % 2 != 0 and lin == 0:
            tabuleiro[lin][col] += 100
            return True
        elif tabuleiro[lin][col] % 2 == 0 and lin == 7:
            tabuleiro[lin][col] += 100
            return True
    return False

def sequenciaCaptura(tabuleiro, lin_peca, col_peca, direcao, cont_pecas_comidas):
    peca_atual = tabuleiro[lin_peca][col_peca]
    eh_dama = ehDama(peca_atual)
    
    movimentos = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
    for dlin, dcol in movimentos:
        if (direcao == dlin or eh_dama) and posicaoValida(lin_peca + dlin, col_peca + dcol) and posicaoValida(lin_peca + 2*dlin, col_peca + 2*dcol):
            meio = tabuleiro[lin_peca + dlin][col_peca + dcol]
            destino = tabuleiro[lin_peca + 2*dlin][col_peca + 2*dcol]
            if meio > 0 and (meio % 2 != peca_atual % 2) and destino == 0:
                tabuleiro[lin_peca + 2*dlin][col_peca + 2*dcol] = peca_atual
                tabuleiro[lin_peca][col_peca] = 0
                tabuleiro[lin_peca + dlin][col_peca + dcol] = 0
                cont_pecas_comidas[0] += 1
                coroarPeca(tabuleiro, lin_peca + 2*dlin, col_peca + 2*dcol)
                sequenciaCaptura(tabuleiro, lin_peca + 2*dlin, col_peca + 2*dcol, direcao, cont_pecas_comidas)
                return

def aplicaMovimento(tabuleiro, lin_peca_idx, col_peca_idx, lin_Destino_idx, col_Destino_idx, direcao):
    cont_pecas_capturadas = [0]
    dlin = lin_Destino_idx - lin_peca_idx
    dcol = abs(col_Destino_idx - col_peca_idx)
    peca_original = tabuleiro[lin_peca_idx][col_peca_idx]

    if abs(dlin) == 2 and dcol == 2:
        lin_capturada = (lin_peca_idx + lin_Destino_idx) // 2
        col_capturada = (col_peca_idx + col_Destino_idx) // 2
        tabuleiro[lin_Destino_idx][col_Destino_idx] = peca_original
        tabuleiro[lin_peca_idx][col_peca_idx] = 0
        tabuleiro[lin_capturada][col_capturada] = 0
        cont_pecas_capturadas[0] = 1
        sequenciaCaptura(tabuleiro, lin_Destino_idx, col_Destino_idx, direcao, cont_pecas_capturadas)
        coroarPeca(tabuleiro, lin_Destino_idx, col_Destino_idx)
        return True
    elif abs(dlin) == 1 and dcol == 1:
        tabuleiro[lin_Destino_idx][col_Destino_idx] = peca_original
        tabuleiro[lin_peca_idx][col_peca_idx] = 0
        coroarPeca(tabuleiro, lin_Destino_idx, col_Destino_idx)
        return True
    return False

def copia_tabuleiro(origem, destino):
    for i in range(8):
        for j in range(8):
            destino[i][j] = origem[i][j]

def calcularForcaTabuleiro(tabuleiro):
    forca_brancas = 0
    forca_pretas = 0
    for lin in range(8):
        for col in range(8):
            if tabuleiro[lin][col] > 0:
                forca_peca = 10
                if tabuleiro[lin][col] % 2 == 0:
                    if posicaoValida(lin + 1, col - 1) and tabuleiro[lin + 1][col - 1] > 0 and tabuleiro[lin + 1][col - 1] % 2 == 0: forca_peca += 2
                    if posicaoValida(lin + 1, col + 1) and tabuleiro[lin + 1][col + 1] > 0 and tabuleiro[lin + 1][col + 1] % 2 == 0: forca_peca += 2
                    if lin == 7: forca_peca += 3
                    forca_brancas += forca_peca
                else:
                    if posicaoValida(lin - 1, col - 1) and tabuleiro[lin - 1][col - 1] > 0 and tabuleiro[lin - 1][col - 1] % 2 != 0: forca_peca += 2
                    if posicaoValida(lin - 1, col + 1) and tabuleiro[lin - 1][col + 1] > 0 and tabuleiro[lin - 1][col + 1] % 2 != 0: forca_peca += 2
                    if lin == 0: forca_peca += 3
                    forca_pretas += forca_peca
    return forca_brancas - forca_pretas

def avaliarTabuleiro(tabuleiro):
    score = 0
    cont_brancas = 0
    cont_pretas = 0
    brancas_avancadas = 0
    pretas_avancadas = 0
    brancas_centro = 0
    pretas_centro = 0
    
    for lin in range(8):
        for col in range(8):
            if tabuleiro[lin][col] > 0:
                if tabuleiro[lin][col] % 2 == 0:
                    cont_brancas += 1
                    if lin >= 4: brancas_avancadas += 1
                    if 2 <= col <= 5: brancas_centro += 1
                else:
                    cont_pretas += 1
                    if lin <= 3: pretas_avancadas += 1
                    if 2 <= col <= 5: pretas_centro += 1
                    
    score = (cont_brancas - cont_pretas) * 10
    score += brancas_avancadas * 2
    score -= pretas_avancadas * 2
    score += brancas_centro
    score -= pretas_centro
    score += calcularForcaTabuleiro(tabuleiro)
    return score

def geraMovimentos(tabuleiro, direcao):
    lista = []
    for lin in range(8):
        for col in range(8):
            peca = tabuleiro[lin][col]
            if peca <= 0: continue
            eh_dama = ehDama(peca)
            
            movimentos_possiveis = []
            if direcao == -1 and peca % 2 != 0: 
                movimentos_possiveis = [(-1, 1), (-1, -1)]
                if eh_dama: movimentos_possiveis.extend([(1, 1), (1, -1)])
            elif direcao == 1 and peca % 2 == 0: 
                movimentos_possiveis = [(1, 1), (1, -1)]
                if eh_dama: movimentos_possiveis.extend([(-1, 1), (-1, -1)])
                
            for dlin, dcol in movimentos_possiveis:
                if posicaoValida(lin + dlin, col + dcol) and tabuleiro[lin + dlin][col + dcol] > 0 and tabuleiro[lin + dlin][col + dcol] % 2 != peca % 2:
                    if posicaoValida(lin + 2*dlin, col + 2*dcol) and tabuleiro[lin + 2*dlin][col + 2*dcol] == 0:
                        lista.append(Movimento(lin, col, lin + 2*dlin, col + 2*dcol))
                elif posicaoValida(lin + dlin, col + dcol) and tabuleiro[lin + dlin][col + dcol] == 0:
                    lista.append(Movimento(lin, col, lin + dlin, col + dcol))
    return lista

def minimax(tabuleiro, profundidade, profundidadeMax, maximizando, direcao):
    if profundidade == profundidadeMax: return avaliarTabuleiro(tabuleiro)
    
    movimentos = geraMovimentos(tabuleiro, 1 if maximizando else -1)
    if len(movimentos) == 0: return avaliarTabuleiro(tabuleiro)
    
    if maximizando:
        alfa = -99999
        for mov in movimentos:
            tabuleiro_temp = [[0 for _ in range(8)] for _ in range(8)]
            copia_tabuleiro(tabuleiro, tabuleiro_temp)
            aplicaMovimento(tabuleiro_temp, mov.linOrig, mov.colOrig, mov.linDest, mov.colDest, 1)
            score = minimax(tabuleiro_temp, profundidade + 1, profundidadeMax, False, -1)
            if score > alfa: alfa = score
        return alfa
    else:
        beta = 99999
        for mov in movimentos:
            tabuleiro_temp = [[0 for _ in range(8)] for _ in range(8)]
            copia_tabuleiro(tabuleiro, tabuleiro_temp)
            aplicaMovimento(tabuleiro_temp, mov.linOrig, mov.colOrig, mov.linDest, mov.colDest, -1)
            score = minimax(tabuleiro_temp, profundidade + 1, profundidadeMax, True, 1)
            if score < beta: beta = score
        return beta


# ==========================================
# 2. INTERFACE STREAMLIT COM VISUAL CHESS.COM
# ==========================================

def aplicar_estilo_chess_com():
    """Injeta CSS no Streamlit para criar o visual profissional do tabuleiro."""
    st.markdown("""
        <style>
        /* Remove o espaço entre as colunas do tabuleiro */
        div[data-testid="column"] {
            padding: 0px !important;
            gap: 0px !important;
        }
        
        /* Estiliza os botões (Casas Verdes - onde o jogo acontece) */
        div.stButton > button {
            height: 70px !important;
            width: 100% !important;
            border-radius: 0px !important; /* Remove as bordas arredondadas */
            border: none !important;
            background-color: #739552 !important; /* Verde Chess.com */
            font-size: 100px !important; /* Tamanho da peça */
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0 !important;
            box-shadow: none !important;
        }
        
        /* Efeito ao passar o mouse na casa verde */
        div.stButton > button:hover {
            background-color: #a9ca7a !important; 
        }

        /* Estilo para as Casas Claras (onde não se joga) */
        .casa-clara {
            background-color: #ebecd0; /* Creme Chess.com */
            height: 70px;
            width: 100%;
            margin: 0;
            padding: 0;
        }
        </style>
    """, unsafe_allow_html=True)

def inicializar_estado():
    if 'tabuleiro' not in st.session_state:
        tabuleiro_inicial = [[0 for _ in range(8)] for _ in range(8)]
        montarTabuleiro(tabuleiro_inicial)
        st.session_state.tabuleiro = tabuleiro_inicial
        st.session_state.turno_jogador = True 
        st.session_state.origem_selecionada = None 
        st.session_state.mensagem = "Sua vez! Selecione uma peça Vermelha (🔴)."

def contar_pecas_estado():
    pretas, brancas = 0, 0
    for l in range(8):
        for c in range(8):
            if st.session_state.tabuleiro[l][c] > 0:
                if st.session_state.tabuleiro[l][c] % 2 == 0: brancas += 1
                else: pretas += 1
    return pretas, brancas

def clique_casa(lin, col):
    if not st.session_state.turno_jogador: return 

    tabuleiro = st.session_state.tabuleiro
    peca_clicada = tabuleiro[lin][col]

    if st.session_state.origem_selecionada is None:
        if peca_clicada > 0 and peca_clicada % 2 != 0: 
            st.session_state.origem_selecionada = (lin, col)
            st.session_state.mensagem = "Peça selecionada. Clique no destino."
        else:
            st.session_state.mensagem = "Por favor, clique em uma de suas peças (Vermelhas)."
    else:
        lin_orig, col_orig = st.session_state.origem_selecionada
        
        if lin_orig == lin and col_orig == col:
            st.session_state.origem_selecionada = None
            st.session_state.mensagem = "Seleção cancelada. Escolha uma peça."
            return

        movimentos_validos = geraMovimentos(tabuleiro, -1)
        movimento_permitido = False
        
        for mov in movimentos_validos:
            if mov.linOrig == lin_orig and mov.colOrig == col_orig and mov.linDest == lin and mov.colDest == col:
                movimento_permitido = True
                break

        if movimento_permitido:
            aplicaMovimento(tabuleiro, lin_orig, col_orig, lin, col, -1)
            st.session_state.origem_selecionada = None
            st.session_state.turno_jogador = False
            st.session_state.mensagem = "A IA está pensando..."
        else:
            st.session_state.origem_selecionada = None
            st.session_state.mensagem = "Movimento inválido! Tente novamente."

def jogada_ia():
    if not st.session_state.turno_jogador:
        movimentos_ia = geraMovimentos(st.session_state.tabuleiro, 1)
        if len(movimentos_ia) == 0:
            st.session_state.mensagem = "IA sem movimentos. Você venceu!"
            return

        movs_captura = [m for m in movimentos_ia if abs(m.linDest - m.linOrig) == 2]
        if movs_captura: movimentos_ia = movs_captura

        melhor_idx = 0
        melhor_score = -99999
        profundidadeMax = 3 

        for i in range(len(movimentos_ia)):
            tab_temp = [[0 for _ in range(8)] for _ in range(8)]
            copia_tabuleiro(st.session_state.tabuleiro, tab_temp)
            aplicaMovimento(tab_temp, movimentos_ia[i].linOrig, movimentos_ia[i].colOrig, movimentos_ia[i].linDest, movimentos_ia[i].colDest, 1)
            s = minimax(tab_temp, 1, profundidadeMax, False, -1)
            if s > melhor_score:
                melhor_score = s
                melhor_idx = i

        mov_escolhido = movimentos_ia[melhor_idx]
        aplicaMovimento(st.session_state.tabuleiro, mov_escolhido.linOrig, mov_escolhido.colOrig, mov_escolhido.linDest, mov_escolhido.colDest, 1)
        
        st.session_state.turno_jogador = True
        st.session_state.mensagem = "Sua vez!"

def main():
    st.set_page_config(page_title="Damas IA - Premium", layout="centered")
    aplicar_estilo_chess_com() # Injeta o nosso CSS mágico!
    inicializar_estado()

    st.title("♟️ Damas Online")
    
    pretas, brancas = contar_pecas_estado()
    col1, col2 = st.columns(2)
    col1.metric("Você (🔴)", pretas)
    col2.metric("Computador (⚪)", brancas)

    if pretas == 0: st.error("A IA venceu! Mais sorte na próxima.")
    elif brancas == 0: st.success("🎉 PARABÉNS! Você venceu a IA!")
    else:
        if st.session_state.turno_jogador: st.info(st.session_state.mensagem)
        else: st.warning(st.session_state.mensagem)

    # Criação do Tabuleiro Visual
    for lin in range(8):
        cols = st.columns(8)
        for col in range(8):
            casa_valida = (lin + col) % 2 != 0
            peca = st.session_state.tabuleiro[lin][col]
            
            # Escolhendo os novos ícones das peças
            simbolo = ""
            if peca > 0:
                if peca % 2 == 0: # Brancas (IA)
                    simbolo = "♔" if ehDama(peca) else "⚪"
                else: # Pretas/Vermelhas (Jogador)
                    simbolo = "♚" if ehDama(peca) else "🔴"

            # Destaca a peça selecionada como se fosse o Chess.com
            if st.session_state.origem_selecionada == (lin, col):
                simbolo = "🟡" # Círculo amarelo indicando seleção

            with cols[col]:
                if casa_valida:
                    # Casa Escura (Verde) -> Botão clicável
                    st.button(simbolo, key=f"btn_{lin}_{col}", on_click=clique_casa, args=(lin, col), use_container_width=True)
                else:
                    # Casa Clara (Creme) -> Bloco HTML sem interação
                    st.markdown("<div class='casa-clara'></div>", unsafe_allow_html=True)

    if not st.session_state.turno_jogador and brancas > 0 and pretas > 0:
        jogada_ia()
        st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Partida", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

if __name__ == "__main__":
    main()

