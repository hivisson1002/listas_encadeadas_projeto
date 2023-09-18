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

        print("Peças de Dominó no início do jogo:")

        while True:
            print(f"\nJogador atual: {jogador_atual + 1}")
            print("Peças no tabuleiro:", [str(peca) for peca in self.tabuleiro])

            peca_valida = False
            tentativas = 0

            while not peca_valida and tentativas < 7:
                self.imprimir_pecas_jogador(jogador_atual)
                peca_a_jogar = int(input("Escolha a peça para jogar (índice da peça) ou 0 para sair: "))

                if peca_a_jogar == 0:
                    print("O jogo foi encerrado.")
                    return

                peca_a_jogar -= 1

                if peca_a_jogar < 0 or peca_a_jogar >= len(self.jogadores[jogador_atual]):
                    print("Índice de peça inválido. Tente novamente.")
                else:
                    peca_escolhida = self.jogadores[jogador_atual][peca_a_jogar]
                    if self.e_jogada_valida(peca_escolhida):
                        self.jogadores[jogador_atual].pop(peca_a_jogar)
                        peca_valida = True
                    else:
                        print("Essa peça não pode ser jogada. Escolha outra.")
                        tentativas += 1

            if peca_valida:
                self.atualizar_tabuleiro(peca_escolhida)
                print(f"\nJogador {jogador_atual + 1} jogou a peça: {str(peca_escolhida)}")
            else:
                print(f"\nJogador {jogador_atual + 1} não pode jogar uma peça e passou para o próximo jogador.")

            if not any(self.jogadores[jogador_atual]):
                print(f"\nJogador {jogador_atual + 1} venceu!")
                break

            jogador_atual = (jogador_atual + 1) % self.num_jogadores

    def e_jogada_valida(self, peca):
        if not self.tabuleiro:
            return True

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

    def imprimir_pecas_jogador(self, jogador):
        print(f"Jogador {jogador + 1}: {[str(peca) for peca in self.jogadores[jogador]]}")

if __name__ == "__main__":
    num_jogadores = 4
    num_pecas_por_jogador = 6
    jogo_domino = DominoGame(num_jogadores, num_pecas_por_jogador)
    jogo_domino.jogar_jogo()
