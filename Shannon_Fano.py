def calcular_frequencias(texto):
    """
    Calcula a frequência de cada símbolo do texto.

    Parâmetros:
        texto (str): Texto de entrada.

    Retorna:
        dict: Dicionário contendo as frequências dos símbolos.
    """

    frequencias = {}

    for caractere in texto:
        frequencias[caractere] = frequencias.get(caractere, 0) + 1

    return frequencias


def dividir_simbolos(simbolos):
    """
    Divide a lista de símbolos em dois grupos com soma das frequências
    o mais equilibrada possível.

    Parâmetros:
        simbolos (list): Lista de tuplas (símbolo, frequência).

    Retorna:
        tuple: Dois grupos de símbolos.
    """

    total = sum(freq for _, freq in simbolos)

    soma = 0
    melhor_indice = 0
    menor_diferenca = float("inf")

    for i in range(len(simbolos)):

        soma += simbolos[i][1]

        diferenca = abs(total - 2 * soma)

        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhor_indice = i

    esquerda = simbolos[:melhor_indice + 1]
    direita = simbolos[melhor_indice + 1:]

    return esquerda, direita


def construir_codigos(simbolos, codigos, codigo_atual=""):
    """
    Constrói recursivamente os códigos de Shannon-Fano.

    Parâmetros:
        simbolos (list): Lista de tuplas (símbolo, frequência).
        codigos (dict): Dicionário onde serão armazenados os códigos.
        codigo_atual (str): Código parcial construído até o momento.
    """

    if len(simbolos) == 1:
        simbolo = simbolos[0][0]
        codigos[simbolo] = codigo_atual if codigo_atual else "0"
        return

    esquerda, direita = dividir_simbolos(simbolos)

    construir_codigos(esquerda, codigos, codigo_atual + "0")
    
    # Continua a divisão recursiva apenas se existir um grupo à direita.
    if direita:
        construir_codigos(direita, codigos, codigo_atual + "1")


def shannon_fano(texto):
    """
    Codifica um texto utilizando o algoritmo de Shannon-Fano.

    Parâmetros:
        texto (str): Texto original.

    Retorna:
        tuple:
            - texto_codificado (str)
            - codigos (dict)
            - frequencias (dict)
    """

    if not texto:
        return "", {}, {}

    frequencias = calcular_frequencias(texto)

    simbolos = sorted(
        frequencias.items(),
        key=lambda item: (-item[1], item[0])
    )

    codigos = {}

    construir_codigos(simbolos, codigos)

    texto_codificado = "".join(codigos[c] for c in texto)

    return texto_codificado, codigos, frequencias


def shannon_fano_decode(texto_codificado, codigos):
    """
    Decodifica um texto comprimido utilizando os códigos de Shannon-Fano.

    Parâmetros:
        texto_codificado (str): Texto em bits.
        codigos (dict): Dicionário de códigos.

    Retorna:
        str: Texto original.
    """

    if not texto_codificado:
        return ""

    codigo_para_simbolo = {
        codigo: simbolo
        for simbolo, codigo in codigos.items()
    }

    resultado = []
    codigo_atual = ""

    for bit in texto_codificado:

        codigo_atual += bit

        if codigo_atual in codigo_para_simbolo:
            resultado.append(codigo_para_simbolo[codigo_atual])
            codigo_atual = ""

    return "".join(resultado)


def main():

    texto = input("Digite um texto: ")

    texto_codificado, codigos, frequencias = shannon_fano(texto)

    texto_decodificado = shannon_fano_decode(
        texto_codificado,
        codigos
    )

    print("\n========== FREQUÊNCIAS ==========")

    for simbolo, freq in sorted(
        frequencias.items(),
        key=lambda x: x[1],
        reverse=True
    ):
        print(f"{simbolo}: {freq}")

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