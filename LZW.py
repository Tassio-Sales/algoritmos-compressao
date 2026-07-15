import math


def inicializar_dicionario():
    """
    Inicializa o dicionário utilizando a tabela ASCII.

    Retorna:
        dict: Dicionário símbolo -> código.
    """

    return {
        chr(i): i
        for i in range(256)
    }


def lzw(texto):
    """
    Realiza a compressão utilizando o algoritmo LZW.

    Parâmetros:
        texto (str): Texto de entrada.

    Retorna:
        tuple:
            codigos (list[int])
            dicionario_final (dict)
    """

    if not texto:
        return [], {}

    dicionario = inicializar_dicionario()

    proximo_codigo = 256

    sequencia = ""

    codigos = []

    for simbolo in texto:

        teste = sequencia + simbolo

        if teste in dicionario:

            sequencia = teste

        else:

            codigos.append(dicionario[sequencia])

            dicionario[teste] = proximo_codigo

            proximo_codigo += 1

            sequencia = simbolo

    if sequencia:

        codigos.append(dicionario[sequencia])

    return codigos, dicionario


def lzw_decode(codigos):
    """
    Reconstrói o texto original utilizando apenas
    a sequência de códigos.

    Parâmetros:
        codigos (list[int]): Lista de códigos.

    Retorna:
        str: Texto reconstruído.
    """

    if not codigos:
        return ""

    dicionario = {
        i: chr(i)
        for i in range(256)
    }

    proximo_codigo = 256

    codigo = codigos[0]

    sequencia = dicionario[codigo]

    resultado = [sequencia]

    for codigo in codigos[1:]:

        if codigo in dicionario:

            entrada = dicionario[codigo]

        elif codigo == proximo_codigo:

            entrada = sequencia + sequencia[0]

        else:

            raise ValueError(
                "Código inválido durante a descompressão."
            )

        resultado.append(entrada)

        dicionario[proximo_codigo] = (
            sequencia + entrada[0]
        )

        proximo_codigo += 1

        sequencia = entrada

    return "".join(resultado)


def imprimir_dicionario(dicionario):
    """
    Exibe apenas as entradas criadas durante
    a execução do algoritmo.
    """

    print("\n========== DICIONÁRIO FINAL ==========\n")

    print(f"Entradas iniciais : 256")
    print(f"Entradas finais   : {len(dicionario)}")
    print(f"Novas entradas    : {len(dicionario) - 256}")

    print("\nNovas sequências adicionadas:\n")

    for sequencia, codigo in sorted(
        dicionario.items(),
        key=lambda item: item[1]
    ):

        if codigo >= 256:

            print(f"{codigo:>3} -> {repr(sequencia)}")


def main():
    """
    Programa principal.
    """

    texto = input("Digite um texto: ")

    codigos, dicionario = lzw(texto)

    texto_reconstruido = lzw_decode(codigos)

    bits_originais = len(texto) * 8

    maior_codigo = max(codigos)

    bits_por_codigo = max(
        1,
        math.ceil(
            math.log2(maior_codigo + 1)
        )
    )

    bits_comprimidos = (
        len(codigos)
        * bits_por_codigo
    )

    economia = (
        bits_originais
        - bits_comprimidos
    )

    taxa = (
        economia
        / bits_originais
    ) * 100

    print("\n========== CÓDIGOS ==========\n")

    print(
        " ".join(
            map(str, codigos)
        )
    )

    print()

    print(
        f"Quantidade de códigos: {len(codigos)}"
    )

    imprimir_dicionario(dicionario)

    print("\n========== RESULTADOS ==========\n")

    print(
        f"Texto original      : {texto}"
    )

    print(
        f"Texto reconstruído  : {texto_reconstruido}"
    )

    print()

    print(
        f"Reconstrução correta: {texto == texto_reconstruido}"
    )

    print("\n========== TAMANHOS ==========\n")

    print(
        f"Texto original      : {len(texto)} caracteres ({bits_originais} bits)"
    )

    print(
        f"Texto comprimido    : {bits_comprimidos} bits"
    )

    print(
        f"Maior código        : {maior_codigo}"
    )

    print(
        f"Bits por código     : {bits_por_codigo}"
    )

    print(
        f"Economia            : {economia} bits"
    )

    print(
        f"Taxa de compressão  : {taxa:.2f}%"
    )


if __name__ == "__main__":
    main()