def rle(texto):
    """
    Comprime uma string utilizando o algoritmo Run-Length Encoding (RLE).

    O algoritmo substitui sequências consecutivas de caracteres iguais
    pelo número de ocorrências seguido do caractere.

    Exemplo:
        "AAAABBCCDAA" -> "4A2B2C1D2A"

    Parâmetros:
        texto (str):
            Texto original a ser comprimido.

    Retorna:
        str:
            Texto comprimido.

    Complexidade:
        Tempo: O(n), pois o texto é percorrido uma única vez.
        Espaço: O(n), devido à construção da saída.
    """

    if not texto:
        return ""

    resultado = []

    caractere_atual = texto[0]
    contador = 1

    # Percorre a string apenas uma vez
    for caractere in texto[1:]:

        if caractere == caractere_atual:
            contador += 1
        else:
            resultado.append(f"{contador}{caractere_atual}")
            caractere_atual = caractere
            contador = 1

    # Adiciona a última sequência
    resultado.append(f"{contador}{caractere_atual}")

    return "".join(resultado)


def rle_decode(texto):
    """
    Descomprime uma string codificada com Run-Length Encoding (RLE).

    O algoritmo interpreta cada sequência numérica encontrada como
    a quantidade de repetições do caractere seguinte.

    Exemplo:
        "4A2B2C1D2A" -> "AAAABBCCDAA"

    Parâmetros:
        texto (str):
            Texto comprimido no formato quantidade + caractere.

    Retorna:
        str:
            Texto original reconstruído.

    Complexidade:
        Tempo: O(n)
        Espaço: O(n)
    """

    if not texto:
        return ""

    resultado = []
    quantidade = ""

    for caractere in texto:
        
        # Acumula todos os dígitos para permitir quantidades maiores que 9
        if caractere.isdigit():
            quantidade += caractere
        else:
            resultado.append(caractere * int(quantidade))
            quantidade = ""

    return "".join(resultado)


def main():
    """
    Executa o programa principal do algoritmo RLE.

    Permite ao usuário informar um texto,
    realiza a compressão, descompressão e apresenta
    as métricas de tamanho e taxa de compressão.
    """

    texto = input("Digite um texto: ")

    texto_comprimido = rle(texto)
    texto_descomprimido = rle_decode(texto_comprimido)

    print("\n========== RESULTADOS ==========")
    print(f"Texto original      : {texto}")
    print(f"Texto comprimido    : {texto_comprimido}")
    print(f"Texto descomprimido : {texto_descomprimido}")

    print("\n========== TAMANHOS ==========")

    # Considera cada caractere representado por 8 bits (ASCII)
    bits_originais = len(texto) * 8
    bits_comprimidos = len(texto_comprimido) * 8
    bits_economizados = bits_originais - bits_comprimidos

    print(f"Texto original: {len(texto)} caracteres ({bits_originais} bits)")
    print(f"Texto comprimido: {len(texto_comprimido)} caracteres ({bits_comprimidos} bits)")
    print(f"Economia: {bits_economizados} bits")

    if len(texto) > 0:
        taxa = (1 - len(texto_comprimido)/len(texto))*100
        print(f"Taxa de compressão  : {taxa:.2f}%")
    else:
        print("Taxa de compressão  : 0.00%")


if __name__ == "__main__":
    main()