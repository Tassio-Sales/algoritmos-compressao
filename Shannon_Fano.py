def calcular_frequencias(texto):
    """
    Calcula a frequência de ocorrência de cada símbolo no texto.

    A frequência dos símbolos é utilizada pelo algoritmo Shannon-Fano
    para determinar quais caracteres receberão códigos binários menores.

    Parâmetros:
        texto (str):
            Texto de entrada.

    Retorna:
        dict:
            Dicionário no formato:
            {símbolo: quantidade_de_ocorrências}.
    """

    frequencias = {}

    for caractere in texto:
        frequencias[caractere] = frequencias.get(caractere, 0) + 1

    return frequencias


def dividir_simbolos(simbolos):
    """
    Divide os símbolos em dois grupos com frequências totais
    aproximadamente iguais.

    Essa divisão é a etapa principal do Shannon-Fano:
    após ordenar os símbolos por frequência, o algoritmo divide
    recursivamente a lista tentando manter as somas dos grupos
    equilibradas.

    Parâmetros:
        simbolos (list):
            Lista de tuplas no formato:
            [(símbolo, frequência), ...]

    Retorna:
        tuple:
            Dois grupos resultantes da divisão.
    """

    # Soma total das frequências para encontrar o ponto de divisão mais equilibrado.    
    total = sum(freq for _, freq in simbolos)

    soma = 0
    melhor_indice = 0
    menor_diferenca = float("inf")

    for i in range(len(simbolos)):

        soma += simbolos[i][1]

        # Calcula a diferença entre os dois grupos. Quanto menor a diferença, mais equilibrada é a divisão.
        diferenca = abs(total - 2 * soma)

        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhor_indice = i

    esquerda = simbolos[:melhor_indice + 1]
    direita = simbolos[melhor_indice + 1:]

    return esquerda, direita


def construir_codigos(simbolos, codigos, codigo_atual=""):
    """
    Gera os códigos binários dos símbolos através da divisão
    recursiva característica do Shannon-Fano.

    A cada divisão:
        - grupo esquerdo recebe o bit 0;
        - grupo direito recebe o bit 1.

    O processo continua até que cada símbolo possua
    seu próprio código.

    Parâmetros:
        simbolos (list):
            Lista de símbolos e suas frequências.

        codigos (dict):
            Estrutura onde os códigos finais serão armazenados.

        codigo_atual (str):
            Código parcial construído durante a recursão.
    """

    if len(simbolos) == 1:
        simbolo = simbolos[0][0]
        codigos[simbolo] = codigo_atual if codigo_atual else "0"
        return
    
    # Divide o conjunto atual para atribuir novos bits aos grupos resultantes.
    esquerda, direita = dividir_simbolos(simbolos)

    # Símbolos do grupo esquerdo recebem o bit 0.
    construir_codigos(esquerda, codigos, codigo_atual + "0")
    
    # Símbolos do grupo direito recebem o bit 1.
    if direita:
        construir_codigos(direita, codigos, codigo_atual + "1")


def shannon_fano(texto):
    """
    Codifica um texto utilizando o algoritmo de Shannon-Fano.

    Parâmetros:
        texto (str): Texto original.

    Retorna:
        tuple:
            - str:
                Sequência de bits resultante da compressão.

            - dict:
                Tabela contendo o código binário de cada símbolo.

            - dict:
                Frequência de ocorrência dos símbolos.
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

    A decodificação percorre a sequência de bits acumulando símbolos
    até encontrar uma sequência existente na tabela de códigos.

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
    """
    Executa um exemplo completo do Shannon-Fano.

    O programa realiza:
        - leitura do texto original;
        - cálculo das frequências;
        - geração dos códigos;
        - compressão;
        - descompressão;
        - comparação dos tamanhos.
    """
    
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