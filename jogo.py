import random

# Define a classe DominoPiece para representar uma peça de dominó.
class DominoPiece:
    def __init__(self, lado1, lado2):
        self.lado1 = lado1
        self.lado2 = lado2
        self.proxima = None  # Referência para a próxima peça na lista.

    def __repr__(self):
        return f'[{self.lado1},{self.lado2}]'

# Define a classe DominoGame para representar o jogo de dominó.
class DominoGame:
    def __init__(self, num_jogadores, num_pecas_por_jogador):
        self.num_jogadores = num_jogadores
        self.num_pecas_por_jogador = num_pecas_por_jogador
        self.jogadores = [None] * num_jogadores  # Inicializa a lista de peças de cada jogador como None.
        self.conjunto_domino = self.criar_conjunto_domino()
        self.embaralhar_e_distribuir_pecas() # Embaralha e distribui as peças para os jogadores.
        self.tabuleiro = [] # Inicializa o tabuleiro vazio.

    def criar_conjunto_domino(self):
        conjunto_domino = [DominoPiece(i, j) for i in range(7) for j in range(i, 7)]
        return conjunto_domino

    def embaralhar_e_distribuir_pecas(self):
        random.shuffle(self.conjunto_domino)
        for jogador in range(self.num_jogadores):
            self.jogadores[jogador] = self.conjunto_domino[:self.num_pecas_por_jogador]
            self.conjunto_domino = self.conjunto_domino[self.num_pecas_por_jogador:]

    def jogar_jogo(self):
        jogador_atual = 0

        print("*** DOMINÓ ***\nInstruções: para sair digite 0 e para pular digite 9.\n\nPeças de Dominó no início do jogo:")

        while True:
            print(f"\nJogador atual: {jogador_atual + 1}")  # Exibe o número do jogador atual.
            print("\nPeças no tabuleiro:", [str(peca) for peca in self.tabuleiro])  # Exibe as peças no tabuleiro.

            peca_valida = False  # Inicializa a variável que verifica se a peça escolhida é válida.
            tentativas = 0  # Inicializa o contador de tentativas.

            while not peca_valida and tentativas < 7:
                self.imprimir_todas_pecas()
                peca_a_jogar = int(input("Escolha o índice da peça ou 9 para pular: "))

                if peca_a_jogar == 0:
                    print("O jogo foi encerrado.")
                    return

                if peca_a_jogar == 9:
                    print(f"Jogador {peca_a_jogar + 1} passou para o próximo jogador.")
                    break

                peca_a_jogar -= 1

                if peca_a_jogar < 0 or peca_a_jogar >= len(self.jogadores[jogador_atual]):
                    print("Índice de peça inválido. Tente novamente.")
                else:
                    peca_escolhida = self.jogadores[jogador_atual][peca_a_jogar]
                    if self.e_jogada_valida(peca_escolhida):
                        self.jogadores[jogador_atual].pop(peca_a_jogar)  # Remove a peça jogada do conjunto do jogador.
                        peca_valida = True
                    else:
                        print("Essa peça não pode ser jogada. Escolha outra.")
                        tentativas += 1

            if peca_valida:
                self.atualizar_tabuleiro(peca_escolhida)  # Atualiza o tabuleiro com a peça escolhida.
                print(f"\nJogador {jogador_atual + 1} jogou a peça: {str(peca_escolhida)}")
                print('Peças após a jogada:')
            else:
                print(f"\nJogador {jogador_atual + 1} não pode jogar uma peça e passou para o próximo jogador.")

            if not any(self.jogadores[jogador_atual]):
                print(f"\nJogador {jogador_atual + 1} venceu!")  # Exibe a mensagem de vitória do jogador.
                break

            jogador_atual = (jogador_atual + 1) % self.num_jogadores  # Avança para o próximo jogador.

    def e_jogada_valida(self, peca):
        if not self.tabuleiro:
            return True

        # Verifica se a peça escolhida pode ser jogada no tabuleiro.
        return peca.lado1 in (self.tabuleiro[0].lado1, self.tabuleiro[-1].lado2) or \
               peca.lado2 in (self.tabuleiro[0].lado1, self.tabuleiro[-1].lado2)

    def atualizar_tabuleiro(self, peca):
        if not self.tabuleiro:
            self.tabuleiro.append(peca)
        elif peca.lado2 == self.tabuleiro[0].lado1:
            self.tabuleiro.insert(0, peca)
        elif peca.lado1 == self.tabuleiro[0].lado1:
            peca.lado2, peca.lado1 = peca.lado1, peca.lado2
            self.tabuleiro.insert(0, peca)
        elif peca.lado2 == self.tabuleiro[0].lado1:
            peca.lado1, peca.lado2 = peca.lado2, peca.lado1
            self.tabuleiro.insert(0, peca)
        elif peca.lado1 == self.tabuleiro[-1].lado2:
            self.tabuleiro.append(peca)
        elif peca.lado2 == self.tabuleiro[-1].lado2:
            peca.lado1, peca.lado2 = peca.lado2, peca.lado1
            self.tabuleiro.append(peca)

    def imprimir_todas_pecas(self):
        for i in range(self.num_jogadores):
            print(f"Jogador {i + 1}: {[str(peca) for peca in self.jogadores[i]]}")

if __name__ == "__main__":
    num_jogadores = 4
    num_pecas_por_jogador = 6
    jogo_domino = DominoGame(num_jogadores, num_pecas_por_jogador)
    jogo_domino.jogar_jogo()
