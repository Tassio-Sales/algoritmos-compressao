import heapq


class NoHuffman:
    """
    Representa um nó da árvore de Huffman.
    """

    def __init__(self, simbolo, frequencia):
        self.simbolo = simbolo
        self.frequencia = frequencia
        self.esquerda = None
        self.direita = None

    def __lt__(self, outro):
        """
        Permite comparar nós pela frequência para utilização no heap.
        """
        return self.frequencia < outro.frequencia


def calcular_frequencias(texto):
    """
    Calcula a frequência de cada símbolo do texto.

    Parâmetros:
        texto (str): Texto de entrada.

    Retorna:
        dict: Frequências dos símbolos.
    """

    frequencias = {}

    for caractere in texto:
        frequencias[caractere] = frequencias.get(caractere, 0) + 1

    return frequencias


def construir_arvore_huffman(frequencias):
    """
    Constrói a árvore de Huffman utilizando uma fila de prioridade.

    Parâmetros:
        frequencias (dict): Frequência dos símbolos.

    Retorna:
        NoHuffman: Raiz da árvore.
    """

    heap = []

    for simbolo, frequencia in frequencias.items():
        heapq.heappush(heap, NoHuffman(simbolo, frequencia))

    if len(heap) == 1:
        return heap[0]

    while len(heap) > 1:

        esquerda = heapq.heappop(heap)
        direita = heapq.heappop(heap)

        pai = NoHuffman(None, esquerda.frequencia + direita.frequencia)
        pai.esquerda = esquerda
        pai.direita = direita

        heapq.heappush(heap, pai)

    return heap[0]


def gerar_codigos(no, codigo_atual="", codigos=None):
    """
    Gera os códigos binários percorrendo a árvore.

    Parâmetros:
        no (NoHuffman): Nó atual.
        codigo_atual (str): Código parcial.
        codigos (dict): Dicionário dos códigos.

    Retorna:
        dict: Dicionário contendo cada símbolo e seu respectivo código binário.
    """

    if codigos is None:
        codigos = {}

    if no is None:
        return codigos

    if no.simbolo is not None:
        codigos[no.simbolo] = codigo_atual if codigo_atual else "0"
        return codigos

    gerar_codigos(no.esquerda, codigo_atual + "0", codigos)
    gerar_codigos(no.direita, codigo_atual + "1", codigos)

    return codigos


def huffman(texto):
    """
    Codifica um texto utilizando Huffman.

    Parâmetros:
        texto (str): Texto original.

    Retorna:
        tuple:
            texto_codificado,
            codigos,
            raiz,
            frequencias
    """

    if not texto:
        return "", {}, None, {}

    frequencias = calcular_frequencias(texto)

    raiz = construir_arvore_huffman(frequencias)

    codigos = gerar_codigos(raiz)

    texto_codificado = "".join(codigos[c] for c in texto)

    return texto_codificado, codigos, raiz, frequencias


def huffman_decode(texto_codificado, raiz):
    """
    Decodifica um texto utilizando a árvore de Huffman.

    Parâmetros:
        texto_codificado (str): Texto codificado.
        raiz (NoHuffman): Raiz da árvore.

    Retorna:
        str: Texto original.
    """

    if raiz is None:
        return ""

    if raiz.esquerda is None and raiz.direita is None:
        return raiz.simbolo * len(texto_codificado)

    resultado = []

    no = raiz

    for bit in texto_codificado:

        if bit == "0":
            no = no.esquerda
        else:
            no = no.direita

        if no.simbolo is not None:
            resultado.append(no.simbolo)
            no = raiz

    return "".join(resultado)


def imprimir_arvore(no, nivel=0, lado="Raiz"):
    """
    Imprime a árvore de Huffman em formato textual.

    Parâmetros:
        no (NoHuffman): Nó atual.
        nivel (int): Profundidade da árvore.
        lado (str): Identificação do ramo.
    """

    if no is None:
        return

    print("    " * nivel + f"{lado}: ", end="")

    if no.simbolo is None:
        print(f"[{no.frequencia}]")
    else:
        print(f"{no.simbolo} ({no.frequencia})")

    imprimir_arvore(no.esquerda, nivel + 1, "0")
    imprimir_arvore(no.direita, nivel + 1, "1")


def main():

    texto = input("Digite um texto: ")

    texto_codificado, codigos, raiz, frequencias = huffman(texto)

    texto_decodificado = huffman_decode(
        texto_codificado,
        raiz
    )

    print("\n========== FREQUÊNCIAS ==========")

    for simbolo, freq in sorted(
        frequencias.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"{simbolo}: {freq}")

    print("\n========== ÁRVORE DE HUFFMAN ==========\n")

    imprimir_arvore(raiz)

    print("\n========== CÓDIGOS ==========")

    for simbolo, codigo in sorted(codigos.items()):
        print(f"{simbolo}: {codigo}")

    print("\n========== RESULTADOS ==========")

    print("Texto original:")
    print(texto)

    print("\nTexto codificado:")
    print(texto_codificado)

    print("\nTexto decodificado:")
    print(texto_decodificado)

    print("\n========== TAMANHOS ==========")

    bits_originais = len(texto) * 8
    bits_economizados = bits_originais - len(texto_codificado)

    print(f"Texto original: {len(texto)} caracteres ({bits_originais} bits)")
    print(f"Texto comprimido: {len(texto_codificado)} bits")
    print(f"Economia: {bits_economizados} bits")

    if len(texto) > 0:
        taxa = (1 - len(texto_codificado) / bits_originais) * 100
        print(f"Taxa de compressão: {taxa:.2f}%")
    else:
        print("Taxa de compressão: 0.00%")


if __name__ == "__main__":
    main()