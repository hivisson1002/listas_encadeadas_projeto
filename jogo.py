import random

class PecaDomino:
    def __init__(self, lado1, lado2):
        self.lado1 = lado1
        self.lado2 = lado2

    def __repr__(self): # Método para representação da peça, retorna uma string com os lados
        return f'[{self.lado1},{self.lado2}]'

class ListaEncadeadaNoh:
    def __init__(self, peca):
        self.peca = peca
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.head = None
        self.tail = None

    def add(self, peca):
        novo_no = ListaEncadeadaNoh(peca)
        if not self.head:
            self.head = novo_no
            self.tail = novo_no
        else:
            self.tail.proximo = novo_no
            self.tail = novo_no

    def remove(self, piece):
        if not self.head:
            return

        if self.head.peca == piece:
            self.head = self.head.proximo
            if not self.head:
                self.tail = None
            return

        atual = self.head
        while atual.proximo and atual.proximo.piece != piece:
            atual = atual.proximo

        if atual.proximo:
            atual.proximo = atual.proximo.proximo
            if not atual.proximo:
                self.tail = atual

class JogoDomino:
    def __init__(self, num_jogadores, num_pecas_por_jogador):
        self.num_jogadores = num_jogadores
        self.num_pecas_por_jogador = num_pecas_por_jogador
        self.jogadores = [ListaEncadeada() for _ in range(num_jogadores)]
        print([ListaEncadeada() for _ in range(num_jogadores)])
        self.conjunto_domino = self.criar_conjunto_domino()
        self.embaralhar_e_distribuir_pecas()
        self.tabuleiro = []

    def criar_conjunto_domino(self):
        conjunto_domino = [PecaDomino(i, j) for i in range(7) for j in range(i, 7)]
        return conjunto_domino

    def embaralhar_e_distribuir_pecas(self):
        random.shuffle(self.conjunto_domino)  # Embaralha o conjunto de dominós
        for i in range(self.num_jogadores):
            self.jogadores[i] = self.conjunto_domino[:self.num_pecas_por_jogador]  # Distribui as peças para cada jogador
            self.conjunto_domino = self.conjunto_domino[self.num_pecas_por_jogador:]  # Atualiza o conjunto de dominós

    def jogar_jogo(self):

        jogador_atual = 0
        print("*** DOMINO ***\nInstruções: Digite 0 para sair ou 9 para pular a sua vez.\n\nDominós no início do jogo:")

        while True:
            print(f"\nJogador atual: {jogador_atual + 1}")

            peca_valida = False
            tentativas = 0

            while not peca_valida and tentativas < 7:
                self.imprimir_todas_pecas()
                print("\nPecas no tabuleiro:", [str(peca) for peca in self.tabuleiro])
                peca_a_jogar = int(input("Escolha o índice da peça ou 9 para passar a vez: "))

                if peca_a_jogar == 0:
                    print("O jogo terminou.")
                    return

                if peca_a_jogar == 9:
                    print(f"Jogador {jogador_atual + 1} passou para o próximo jogador.")
                    break

                peca_a_jogar -= 1

                if peca_a_jogar < 0 or peca_a_jogar >= len(self.jogadores[jogador_atual]):
                    print("Índice de peça inválido. Tente novamente.")
                else:
                    peca_escolhida = self.jogadores[jogador_atual][peca_a_jogar]
                    if self.movimento_valido(peca_escolhida):
                        self.jogadores[jogador_atual].pop(peca_a_jogar)
                        peca_valida = True
                    else:
                        print("Essa peça não pode ser jogada. Escolha outra.")
                    tentativas += 1

            if peca_valida:
                self.adicionar_ao_tabuleiro(peca_escolhida)
                print(f"\nJogador {jogador_atual + 1} jogou a peça: {str(peca_escolhida)}")
                print('Peças após a jogada:')
            else:
                print(f"\nJogador {jogador_atual + 1} não pôde jogar e passou para o próximo jogador.")

            if not any(self.jogadores[jogador_atual]):
                print(f"\nJogador {jogador_atual + 1} venceu!")
                break

            jogador_atual = (jogador_atual + 1) % self.num_jogadores  # Atualiza o jogador atual para o próximo jogador

    def movimento_valido(self, peca):
        if not self.tabuleiro:
            return True

        return peca.lado1 in (self.tabuleiro[0].lado1, self.tabuleiro[-1].lado2) or \
               peca.lado2 in (self.tabuleiro[0].lado1, self.tabuleiro[-1].lado2)

    def adicionar_ao_tabuleiro(self, peca):
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
    jogo_domino = JogoDomino(num_jogadores, num_pecas_por_jogador)  # Cria uma instância do jogo de dominó
    jogo_domino.jogar_jogo()
