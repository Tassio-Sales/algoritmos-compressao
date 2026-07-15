import math

ASCII_INICIAL = 256


def inicializar_dicionario():
    """
    Cria o dicionário inicial utilizado pelo algoritmo LZW.

    Inicialmente, o dicionário contém apenas os 256 símbolos
    da tabela ASCII, cada um associado ao seu respectivo código.

    Novas sequências de caracteres serão adicionadas durante
    o processo de compressão.

    Retorna:
        dict:
            Dicionário no formato:
            {símbolo: código}.
    """

    # Cada caractere ASCII recebe inicialmente o seu próprio código numérico.
    return {
        chr(i): i
        for i in range(ASCII_INICIAL)
    }


def lzw(texto):
    """
    Comprime um texto utilizando o algoritmo LZW.

    O algoritmo inicia com um dicionário contendo todos os
    caracteres ASCII e, durante a leitura do texto, adiciona
    novas sequências de caracteres ao dicionário.

    Sempre que uma sequência ainda não estiver cadastrada,
    o código da maior sequência conhecida é emitido e a nova
    sequência passa a fazer parte do dicionário.

    O dicionário é construído dinamicamente durante a compressão,
    não sendo necessário transmiti-lo juntamente com os dados
    comprimidos, pois ele pode ser reconstruído durante a
    descompressão.

    Parâmetros:
        texto (str):
            Texto original.

    Retorna:
        tuple:

            - list[int]:
                Sequência de códigos produzida.

            - dict:
                Dicionário final após a compressão.
    """

    if not texto:
        return [], {}

    # Inicializa o dicionário com os símbolos ASCII.
    dicionario = inicializar_dicionario()

    # Primeiro código disponível para novas sequências.
    proximo_codigo = ASCII_INICIAL

    sequencia = ""

    codigos = []

    for simbolo in texto:

        # Forma uma nova sequência adicionando o símbolo atual à maior sequência conhecida até o momento.
        teste = sequencia + simbolo

        # A sequência já existe no dicionário: continua acumulando caracteres.
        if teste in dicionario:

            sequencia = teste

        else:

            # Como a nova sequência ainda não existe no dicionário, 
            # emite apenas o código da maior sequência já conhecida.
            codigos.append(dicionario[sequencia])

            # A nova sequência passa a fazer parte do dicionário para que possa ser representada 
            # por um único código caso apareça novamente.
            dicionario[teste] = proximo_codigo

            proximo_codigo += 1

            # Reinicia a sequência a partir do símbolo atual.
            sequencia = simbolo
    
    # Emite o código da última sequência processada.
    if sequencia:

        codigos.append(dicionario[sequencia])

    return codigos, dicionario


def lzw_decode(codigos):
    """
    Reconstrói o texto original a partir da sequência
    de códigos produzida pelo algoritmo LZW.

    O dicionário é reconstruído dinamicamente durante
    a decodificação, seguindo exatamente as mesmas regras
    utilizadas na compressão.

    Parâmetros:
        codigos (list[int]):
            Lista de códigos LZW.

    Retorna:
        str:
            Texto reconstruído.
    """

    if not codigos:
        return ""
    
    # Inicializa o dicionário com os símbolos ASCII.
    dicionario = {
        i: chr(i)
        for i in range(ASCII_INICIAL)
    }

    proximo_codigo = ASCII_INICIAL

    codigo = codigos[0]

    # Primeiro código sempre representa uma entrada existente.
    sequencia = dicionario[codigo]

    resultado = [sequencia]
    
    for codigo in codigos[1:]:

        # Código já conhecido pelo dicionário.
        if codigo in dicionario:

            entrada = dicionario[codigo]

        # Caso especial do LZW: 
        # O código ainda não foi inserido no dicionário, 
        # Mas pode ser reconstruído como: sequência + primeiro caractere da própria sequência.
        elif codigo == proximo_codigo:

            entrada = sequencia + sequencia[0]

        else:

            raise ValueError(
                "Código inválido durante a descompressão."
            )

        resultado.append(entrada)

        # Reconstrói exatamente a mesma entrada adicionada pelo compressor, 
        # mantendo ambos os dicionários sincronizados.
        dicionario[proximo_codigo] = (
            sequencia + entrada[0]
        )

        proximo_codigo += 1

        sequencia = entrada

    return "".join(resultado)


def imprimir_dicionario(dicionario):
    """
    Exibe as novas entradas adicionadas ao dicionário
    durante a compressão.

    As 256 entradas iniciais da tabela ASCII não são
    impressas, pois fazem parte da inicialização do algoritmo.

    Função utilizada apenas para fins de visualização.
    """

    print("\n========== DICIONÁRIO FINAL ==========\n")

    print(f"Entradas iniciais : {ASCII_INICIAL}")
    print(f"Entradas finais   : {len(dicionario)}")
    print(f"Novas entradas    : {len(dicionario) - ASCII_INICIAL}")

    print("\nNovas sequências adicionadas:\n")

    for sequencia, codigo in sorted(
        dicionario.items(),
        key=lambda item: item[1]
    ):

        if codigo >= ASCII_INICIAL:

            print(f"{codigo:>3} -> {repr(sequencia)}")


def main():
    """
    Executa um exemplo completo do algoritmo LZW.

    O programa realiza:

        - leitura do texto;

        - compressão;

        - reconstrução do texto;

        - exibição dos códigos gerados;

        - exibição do dicionário criado;

        - comparação dos tamanhos.
    """

    texto = input("Digite um texto: ")

    codigos, dicionario = lzw(texto)

    texto_reconstruido = lzw_decode(codigos)

    bits_originais = len(texto) * 8

    if codigos:
        maior_codigo = max(codigos)
    else:
        maior_codigo = ASCII_INICIAL - 1

    # Estima quantos bits são necessários para representar o maior código gerado pelo algoritmo.
    # Todos os códigos são considerados com esse tamanho para fins de comparação.
    bits_por_codigo = max(
        1,
        math.ceil(
            math.log2(maior_codigo + 1)
        )
    )

    # Estimativa do tamanho da sequência comprimida.
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