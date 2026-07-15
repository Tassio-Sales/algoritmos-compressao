# ============================
# Classes
# ============================

class NoHuffmanAdaptativo:
    """
    Representa um nó da árvore do Huffman Adaptativo.

    Atributos:
        simbolo (str): Símbolo armazenado no nó.
                       None representa o nó NYT.

        peso (int): Quantidade de ocorrências do símbolo.

        esquerda: Filho esquerdo do nó.

        direita: Filho direito do nó.

        pai: Referência ao nó pai.

        ordem (int): Número de ordem utilizado na atualização
                     da árvore.
    """

    def __init__(self, simbolo=None, peso=0, ordem=0):

        self.simbolo = simbolo

        self.peso = peso

        self.esquerda = None

        self.direita = None

        self.pai = None

        self.ordem = ordem


    def eh_folha(self):
        """
        Verifica se o nó é uma folha.

        Retorna:
            True caso não possua filhos.
        """

        return (
            self.esquerda is None and
            self.direita is None
        )


    def eh_nyt(self):
        """
        Verifica se o nó representa o NYT
        (Not Yet Transmitted).

        O NYT é representado por um nó folha
        sem símbolo e peso zero.
        """

        return (
            self.eh_folha()
            and
            self.simbolo is None
        )
    
class ArvoreAdaptive:
    """
    Representa toda a árvore do Huffman Adaptativo.
    """

    def __init__(self):

        self.raiz = criar_arvore_inicial()

        self.nyt = self.raiz

        self.proxima_ordem = 512   

# ============================
# Construção inicial
# ============================

def criar_arvore_inicial():
    """
    Cria a árvore inicial do Huffman Adaptativo.

    No início da compressão a árvore contém
    apenas o nó NYT.

    Estrutura inicial:

            NYT

    Retorna:
        NoHuffmanAdaptativo:
            Nó raiz da árvore.
    """

    raiz = NoHuffmanAdaptativo(
        simbolo=None,
        peso=0,
        ordem=512
    )

    return raiz

# ============================
# Busca e navegação
# ============================

def buscar_no(no, simbolo):
    """
    Procura o nó correspondente a um símbolo.

    Parâmetros:
        no (NoAdaptive): Nó atual.
        simbolo (str): Símbolo procurado.

    Retorna:
        NoAdaptive ou None.
    """

    if no is None:
        return None

    if no.simbolo == simbolo:
        return no

    encontrado = buscar_no(
        no.esquerda,
        simbolo
    )

    if encontrado is not None:
        return encontrado

    return buscar_no(
        no.direita,
        simbolo
    )

def listar_nos(no, lista=None):
    """
    Percorre a árvore e retorna uma lista contendo
    todos os nós.

    Parâmetros:
        no (NoHuffmanAdaptativo)

        lista (list):
            Utilizada na recursão.

    Retorna:
        list
    """

    if lista is None:
        lista = []

    if no is None:
        return lista

    lista.append(no)

    listar_nos(
        no.esquerda,
        lista
    )

    listar_nos(
        no.direita,
        lista
    )

    return lista

def eh_ancestral(ancestral, no):
    """
    Verifica se um nó é ancestral de outro.
    """

    atual = no

    while atual is not None:

        if atual == ancestral:
            return True

        atual = atual.pai

    return False

# ============================
# Operações FGK
# ============================

def encontrar_maior_ordem(raiz, peso, ignorar):
    """
    Procura o nó de maior ordem que possui
    o mesmo peso.

    Parâmetros:
        raiz:
            Raiz da árvore.

        peso:
            Peso procurado.

        ignorar:
            Nó que não pode ser retornado.

    Retorna:
        NoHuffmanAdaptativo ou None.
    """

    lista = []

    listar_nos(
        raiz,
        lista
    )

    candidato = None

    for no in lista:

        if no == ignorar:
            continue

        if no.peso != peso:
            continue

        if (
            candidato is None
            or
            no.ordem > candidato.ordem
        ):
            candidato = no

    return candidato

def encontrar_no_para_troca(raiz, no):

    """
    Procura o líder do bloco
    que pode ser trocado.
    """

    candidato = encontrar_maior_ordem(
        raiz,
        no.peso,
        no
    )

    if candidato is None:
        return None

    if candidato == no:
        return None

    if eh_ancestral(no, candidato):
        return None

    if eh_ancestral(candidato, no):
        return None

    return candidato

def trocar_nos(no1, no2):
    """
    Troca a posição de dois nós na árvore.

    Apenas os ponteiros dos pais são
    atualizados.

    Parâmetros:
        no1
        no2
    """

    if (
        no1 is None or
        no2 is None or
        no1 == no2
    ):
        return

    pai1 = no1.pai
    pai2 = no2.pai

    if pai1 is None or pai2 is None:
        return

    if pai1.esquerda == no1:
        pai1.esquerda = no2
    else:
        pai1.direita = no2

    if pai2.esquerda == no2:
        pai2.esquerda = no1
    else:
        pai2.direita = no1

    no1.pai = pai2
    no2.pai = pai1

    no1.ordem, no2.ordem = (
        no2.ordem,
        no1.ordem
    )

def atualizar_arvore(raiz, no):
    """
    Atualiza a árvore seguindo a ideia do
    algoritmo FGK.

    Para cada nó até a raiz:

        1. procura um nó de mesmo peso
           com maior número de ordem;

        2. caso exista, realiza a troca;

        3. incrementa o peso;

        4. sobe para o pai.
    """

    atual = no

    while atual is not None:        

        candidato = encontrar_no_para_troca(
            raiz,
            atual
        )
        
        if candidato is not None:

            trocar_nos(
                atual,
                candidato
            )

        atual.peso += 1

        atual = atual.pai

# ============================
# Operações auxiliares
# ============================

def obter_codigo(no):
    """
    Obtém o código binário correspondente
    ao caminho da raiz até o nó informado.

    Convenção:

        esquerda -> 0
        direita  -> 1

    Parâmetros:
        no (NoHuffmanAdaptativo)

    Retorna:
        str
    """

    codigo = []

    atual = no

    while atual.pai is not None:

        if atual == atual.pai.esquerda:

            codigo.append("0")

        else:

            codigo.append("1")

        atual = atual.pai

    codigo.reverse()

    return "".join(codigo)

def ascii_8_bits(simbolo):
    """
    Converte um caractere para ASCII em 8 bits.

    Parâmetros:
        simbolo (str)

    Retorna:
        str
    """

    return format(
        ord(simbolo),
        "08b"
    )

def decodificar_simbolo(arvore, bits, indice):
    """
    Decodifica um único símbolo da sequência de bits.

    Retorna:
        tuple:
            (símbolo decodificado, novo índice)
    """

    atual = arvore.raiz


    while not atual.eh_folha():

        if indice >= len(bits):
            raise ValueError(
                "Sequência de bits inválida."
            )

        if bits[indice] == "0":

            atual = atual.esquerda

        elif bits[indice] == "1":

            atual = atual.direita

        else:

            raise ValueError(
                "Bit inválido encontrado."
            )

        indice += 1


    if atual.eh_nyt():

        if indice + 8 > len(bits):

            raise ValueError(
                "Sequência de bits inválida."
            )


        ascii_bits = bits[
            indice:
            indice + 8
        ]


        simbolo = chr(
            int(ascii_bits, 2)
        )


        indice += 8


    else:

        simbolo = atual.simbolo


    return (
        simbolo,
        indice
    )
# ============================
# Inserção e atualização
# ============================
    
def inserir_novo_simbolo(nyt, simbolo, proxima_ordem):
    """
    Insere um novo símbolo na árvore.

    O nó NYT deixa de ser folha e passa a possuir
    dois filhos:

        esquerda -> novo NYT
        direita  -> símbolo

    Retorna:
        tuple:
            (novo_no_simbolo, novo_nyt)
    """

    novo_nyt = NoHuffmanAdaptativo(
        simbolo=None,
        peso=0,
        ordem=proxima_ordem - 2
    )

    novo_simbolo = NoHuffmanAdaptativo(
        simbolo=simbolo,
        peso=0,
        ordem=proxima_ordem - 1
    )

    nyt.esquerda = novo_nyt
    nyt.direita = novo_simbolo

    novo_nyt.pai = nyt
    novo_simbolo.pai = nyt

    nyt.simbolo = None
    nyt.peso = 0

    return (
        novo_simbolo,
        novo_nyt
    )

def inserir_simbolo(arvore, simbolo):
    """
    Processa um símbolo durante a compressão.

    Se o símbolo já existir na árvore:

        • emite seu código atual;
        • atualiza a árvore.

    Caso contrário:

        • emite o código do NYT;
        • emite o ASCII (8 bits) do símbolo;
        • insere o símbolo na árvore;
        • atualiza a árvore.

    Parâmetros:
        arvore (ArvoreAdaptive)

        simbolo (str)

    Retorna:
        str:
            Sequência de bits produzida.
    """

    no = buscar_no(
        arvore.raiz,
        simbolo
    )

    # -----------------------------------
    # Símbolo já conhecido
    # -----------------------------------

    if no is not None:

        codigo = obter_codigo(
            no
        )

        atualizar_arvore(
            arvore.raiz,
            no
        )

        return codigo

    # -----------------------------------
    # Novo símbolo
    # -----------------------------------

    codigo_nyt = obter_codigo(
        arvore.nyt
    )

    codigo_ascii = ascii_8_bits(
        simbolo
    )

    novo_no, novo_nyt = inserir_novo_simbolo(
        arvore.nyt,
        simbolo,
        arvore.proxima_ordem
    )

    arvore.nyt = novo_nyt

    arvore.proxima_ordem -= 2

    atualizar_arvore(
        arvore.raiz,
        novo_no
    )

    return (
        codigo_nyt
        +
        codigo_ascii
    )

def atualizar_simbolo_decodificado(arvore, simbolo):
    """
    Atualiza a árvore após receber
    um símbolo durante a decodificação.
    """

    no = buscar_no(
        arvore.raiz,
        simbolo
    )

    if no is not None:

        atualizar_arvore(
            arvore.raiz,
            no
        )

        return


    novo_no, novo_nyt = inserir_novo_simbolo(
        arvore.nyt,
        simbolo,
        arvore.proxima_ordem
    )

    arvore.nyt = novo_nyt

    arvore.proxima_ordem -= 2

    atualizar_arvore(
        arvore.raiz,
        novo_no
    )

# ============================
# Compressão / Descompressão
# ============================

def adaptive_huffman(texto):
    """
    Realiza a compressão utilizando
    Huffman Adaptativo.
    """

    arvore = ArvoreAdaptive()

    bits_saida = []

    for simbolo in texto:

        bits_saida.append(
            inserir_simbolo(
                arvore,
                simbolo
            )
        )

    return (
        "".join(bits_saida),
        arvore
    )

def adaptive_huffman_decode(bits):
    """
    Reconstrói o texto original a partir da sequência
    de bits produzida pelo Huffman Adaptativo.
    """

    arvore = ArvoreAdaptive()

    indice = 0

    texto = []


    while indice < len(bits):

        simbolo, indice = decodificar_simbolo(
            arvore,
            bits,
            indice
        )


        texto.append(simbolo)


        atualizar_simbolo_decodificado(
            arvore,
            simbolo
        )


    return "".join(texto)


# ============================
# Testes
# ============================

def imprimir_arvore(no, nivel=0):
    """
    Exibe a árvore de forma hierárquica.

    Utilizada apenas para testes.

    Parâmetros:
        no:
            Nó atual.

        nivel:
            Profundidade do nó.
    """

    if no is None:
        return


    espaco = "   " * nivel


    if no.eh_nyt():

        print(
            espaco + "NYT"
        )

    elif no.simbolo is not None:

        print(
            espaco +
            f"{repr(no.simbolo)} "
            f"(peso={no.peso})"
        )

    else:

        print(
            espaco +
            f"* (peso={no.peso})"
        )


    imprimir_arvore(
        no.esquerda,
        nivel + 1
    )

    imprimir_arvore(
        no.direita,
        nivel + 1
    )

def tamanho_arvore(no):
    """
    Calcula a quantidade de nós da árvore.

    Parâmetros:
        no:
            Nó raiz.

    Retorna:
        int:
            Número total de nós.
    """

    if no is None:

        return 0


    return (
        1
        +
        tamanho_arvore(no.esquerda)
        +
        tamanho_arvore(no.direita)
    )


def main():

    texto = input("Digite um texto: ")

    bits, arvore = adaptive_huffman(
        texto
    )

    texto_reconstruido = adaptive_huffman_decode(
        bits
    )

    print("\nBits produzidos:\n")
    print(bits)

    print("\nQuantidade de bits:")
    print(len(bits))

    print("\nTamanho da árvore:")
    print(tamanho_arvore(arvore.raiz))

    print("\nÁrvore Huffman Adaptativa:")
    imprimir_arvore(
        arvore.raiz
    )


    print("\nTexto reconstruído:")
    print(texto_reconstruido)

    print("\nReconstrução correta:")
    print(texto == texto_reconstruido)

if __name__ == "__main__":
    main()