# 🏁 Jogo de Damas com Inteligência Artificial (Algoritmo MiniMax)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![AI Engine](https://img.shields.io/badge/AI-MiniMax%20Algorithm-8E44AD.svg?style=for-the-badge)](https://en.wikipedia.org/wiki/Minimax)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

> Uma implementação completa e estilizada do clássico **Jogo de Damas**, desenvolvida em Python. O projeto conta com um **Bot de IA inteligente alimentado pelo algoritmo de busca MiniMax** e uma interface web moderna inspirada no estilo *Chess.com* construída em **Streamlit**.

---

## 🎯 Sobre o Projeto

Este projeto une teoria dos jogos, estruturas de dados avançadas e inteligência artificial para criar uma experiência envolvente de Jogo de Damas. O grande destaque é a **Engine de IA baseada no Algoritmo MiniMax**, que simula e avalia árvores de jogadas em profundidade para tomar as decisões mais estratégicas contra o jogador humano.

### 🌟 Destaques do Projeto
- 🧠 **Bot Inteligente com MiniMax:** Tomada de decisão em árvore de possibilidades com função de avaliação heurística customizada.
- 🎨 **Interface Web Moderna (Streamlit):** Tabuleiro estilizado em dark mode inspirado no *Chess.com*, com seleção interativa de peças e movimentação por clique.
- ⚔️ **Regras Oficiais de Damas:** Suporte a capturas simples, capturas em sequência, promoção a Dama (coroação) e controle rigoroso de movimentos válidos.
- 💻 **Modo CLI / Terminal:** Engine portátil que também permite jogar diretamente pela linha de comando.

---

## 🧠 Como Funciona a Inteligência Artificial (MiniMax)

O bot utiliza o **Algoritmo MiniMax**, um método fundamental da teoria dos jogos para tomada de decisão em jogos de soma zero de dois jogadores (*Zero-Sum Games*).

```text
                        (Estado Atual do Tabuleiro)
                                    │
                         [ MiniMax - Turno da IA ]  ◄── Maximiza a pontuação
                                  /       \
                                 /         \
                 (Movimento A da IA)     (Movimento B da IA)
                         /                       \
             [ Turno do Jogador ]                [ Turno do Jogador ]  ◄── Minimiza a pontuação
                  /        \                          /        \
             (Resposta) (Resposta)                (Resposta) (Resposta)
                 │          │                         │          │
           [ Avaliação ] [ Avaliação ]          [ Avaliação ] [ Avaliação ]
```

### 📊 Função de Avaliação Heurística (`avaliarTabuleiro`)
A cada nó da árvore de decisão, a IA calcula a força do tabuleiro ponderando:
1. **Contagem e Peso das Peças:** Peças normais vs. Damas (as Damas possuem valor tático muito mais elevado).
2. **Posicionamento Estratégico:** Valorização de controle do centro do tabuleiro e proteção das linhas de base.
3. **Mobilidade e Oportunidades de Captura:** Incentivo a jogadas que forçam a eliminação de peças adversárias e dominam posições-chave.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Interface Gráfica:** Streamlit (CSS Customizado)
- **Estruturas de Dados:** Matrizes bidimensionais para o tabuleiro, gerenciamento de estado via `session_state` e árvores de busca recursiva
- **Algoritmo de IA:** MiniMax com busca heurística

---

## 📂 Estrutura do Repositório

```text
Damas/
├── app_damas.py     # Aplicação Web interativa construída com Streamlit
├── Tabuleiro.py     # Engine principal com regras do jogo, CLI e algoritmo MiniMax
├── requirements.txt # Dependências do projeto (Streamlit, etc.)
└── README.md        # Documentação do projeto
```

---

## 🚀 Como Executar o Projeto

### 📋 Pré-requisitos
Certifique-se de ter o **Python 3.10 ou superior** instalado.

### 1. Clonar o Repositório
```bash
git clone https://github.com/HenriqueRoyale/Damas.git
cd Damas
```

### 2. Instalar as Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o Jogo

#### 🌐 Modo 1: Interface Web (Streamlit - Recomendado)
Execute o comando abaixo para abrir a interface no seu navegador:
```bash
streamlit run app_damas.py
```

#### 💻 Modo 2: Linha de Comando (Terminal CLI)
Para jogar diretamente pelo terminal:
```bash
python Tabuleiro.py
```

---

## 🎮 Como Jogar (Interface Web)

1. Abra a aplicação no seu navegador executando `streamlit run app_damas.py`.
2. Clique na **peça que deseja mover** (ela será destacada no tabuleiro).
3. Clique na **casa de destino desejada**.
4. Após o seu movimento, o **Bot MiniMax** processará o tabuleiro e responderá com a melhor jogada estratégica!

---

## 👤 Autor

**Henrique Royale**  
* Estudante de Ciência de Dados e Inteligência Artificial na PUC-Campinas  
* GitHub: [@HenriqueRoyale](https://github.com/HenriqueRoyale)
```

---

### 💡 Dica Extra para o seu projeto Damas:
Como o seu projeto usa **Streamlit**, você pode subir ele gratuitamente no **[Streamlit Community Cloud](https://streamlit.io/cloud)** em menos de 2 minutos conectando com a sua conta do GitHub! Depois é só colocar o link do site funcionando no campo **Website / About** do repositório no GitHub para qualquer recrutador jogar direto do navegador sem precisar baixar nada!
