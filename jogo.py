import random

class PecaDomino:
    def __init__(self, lado1, lado2):
        self.lado1 = lado1
        self.lado2 = lado2

    def __repr__(self):
        return f'[{self.lado1},{self.lado2}]'

class ListaEncadeadaNoh:
    def __init__(self, peca):
        self.peca = peca
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def add(self, peca):
        novo_no = ListaEncadeadaNoh(peca)
        if not self.head:
            self.head = novo_no
            self.tail = novo_no
        else:
            self.tail.proximo = novo_no
            self.tail = novo_no

    def remove(self, peca):
        if not self.head:
            return

        if self.head.peca == peca:
            self.head = self.head.proximo
            if not self.head:
                self.tail = None
            return

        atual = self.head
        while atual.proximo and atual.proximo.peca != peca:
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
        self.conjunto_domino = self.criar_conjunto_domino()
        self.embaralhar_e_distribuir_pecas()
        self.tabuleiro = []

    def criar_conjunto_domino(self):
        conjunto_domino = [PecaDomino(i, j) for i in range(7) for j in range(i, 7)]
        return conjunto_domino

    def embaralhar_e_distribuir_pecas(self):
        random.shuffle(self.conjunto_domino)
        for i in range(self.num_jogadores):
            for _ in range(self.num_pecas_por_jogador):
                peca = self.conjunto_domino.pop(0)
                self.jogadores[i].add(peca)

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

                if peca_a_jogar < 0:
                    print("Índice de peça inválido. Tente novamente.")
                elif peca_a_jogar == 0:
                    print("O jogo terminou.")
                    return
                elif peca_a_jogar == 9:
                    print(f"Jogador {jogador_atual + 1} passou para o próximo jogador.")
                    break
                else:
                    peca_a_jogar -= 1
                    noh_atual = self.jogadores[jogador_atual].head
                    contar = 0
                    while noh_atual and contar < peca_a_jogar:
                        noh_atual = noh_atual.proximo
                        contar += 1

                    if noh_atual and self.movimento_valido(noh_atual.peca):
                        peca_escolhida = noh_atual.peca
                        self.jogadores[jogador_atual].remove(noh_atual.peca)
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

            if self.jogadores[jogador_atual].is_empty():
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
            current_node = self.jogadores[i].head
            print(f"Jogador {i + 1}: ", end="")
            while current_node:
                print(str(current_node.peca), end=" ")
                current_node = current_node.proximo
            print()

if __name__ == "__main__":
    num_jogadores = 4
    num_pecas_por_jogador = 6
    jogo_domino = JogoDomino(num_jogadores, num_pecas_por_jogador)
    jogo_domino.jogar_jogo()
