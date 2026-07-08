from Run_Length_Encoding import rle, rle_decode
from Shannon_Fano import shannon_fano, shannon_fano_decode
from Huffman import huffman, huffman_decode


def calcular_taxa_compressao(tamanho_original, tamanho_comprimido):
    """
    Calcula a taxa de compressão.

    Parâmetros:
        tamanho_original (int): Tamanho do texto original.
        tamanho_comprimido (int): Tamanho após a compressão.

    Retorna:
        float: Percentual de compressão obtido.
    """

    if tamanho_original == 0:
        return 0.0

    return (1 - (tamanho_comprimido / tamanho_original)) * 100

def classificar_desempenho(taxa):
    """
    Classifica o desempenho da compressão.

    Parâmetros:
        taxa (float): Taxa de compressão.

    Retorna:
        str: Classificação do desempenho.
    """

    if taxa >= 70:
        return "Excelente"

    if taxa >= 40:
        return "Bom"

    if taxa >= 0:
        return "Regular"

    return "Pouco eficiente"

def comparar_algoritmos(texto):
    """
    Executa os três algoritmos e exibe uma comparação dos resultados.

    Parâmetros:
        texto (str): Texto de entrada.
    """

    print("\n" + "=" * 120)
    print("Texto original:")
    print(texto)
    print("=" * 120)

    caracteres_originais = len(texto)
    bits_originais = caracteres_originais * 8

    # ==========================================================
    # RLE
    # ==========================================================

    rle_codificado = rle(texto)
    rle_decodificado = rle_decode(rle_codificado)

    caracteres_rle = len(rle_codificado)

    taxa_rle = calcular_taxa_compressao(
        caracteres_originais,
        caracteres_rle
    )

    economia_rle = caracteres_originais - caracteres_rle
    if economia_rle >= 0:
        economia_rle_texto = f"{economia_rle} caracteres"
    else:
        economia_rle_texto = f"{economia_rle} caracteres"

    observacao_rle = classificar_desempenho(taxa_rle)
    

    # ==========================================================
    # Shannon-Fano
    # ==========================================================

    sf_codificado, sf_codigos, _ = shannon_fano(texto)

    sf_decodificado = shannon_fano_decode(sf_codificado, sf_codigos)

    bits_sf = len(sf_codificado)

    taxa_sf = calcular_taxa_compressao(
        bits_originais,
        bits_sf
    )

    economia_sf = bits_originais - bits_sf
    if economia_sf >= 0:
        economia_sf_texto = f"{economia_sf} bits"
    else:
        economia_sf_texto = f"{economia_sf} bits"
    observacao_sf = classificar_desempenho(taxa_sf)

    # ==========================================================
    # Huffman
    # ==========================================================

    hf_codificado, _, hf_raiz, _ = huffman(texto)

    hf_decodificado = huffman_decode(
        hf_codificado,
        hf_raiz
    )

    bits_hf = len(hf_codificado)

    taxa_hf = calcular_taxa_compressao(
        bits_originais,
        bits_hf
    )

    economia_hf = bits_originais - bits_hf
    if economia_hf >= 0:
        economia_hf_texto = f"{economia_hf} bits"
    else:
        economia_hf_texto = f"{economia_hf} bits"
    observacao_hf = classificar_desempenho(taxa_hf)

    # ==========================================================
    # Tabela
    # ==========================================================

    print("\nTabela Comparativa\n")

    print("=" * 120)

    print(
        f"{'Algoritmo':<18}"
        f"{'Original':>15}"
        f"{'Comprimido':>18}"
        f"{'Economia obtida':>22}"
        f"{'Taxa (%)':>15}"
        f"{'Observação':>29}"
    )

    print("=" * 120)

    print(
        f"{'RLE':<18}"
        f"{str(caracteres_originais) + ' caracteres':>22}"
        f"{str(caracteres_rle) + ' caracteres':>22}"
        f"{economia_rle_texto:>22}"
        f"{taxa_rle:>12.2f}"
        f"{observacao_rle:>22}"
    )

    print(
        f"{'Shannon-Fano':<18}"
        f"{str(bits_originais) + ' bits':>22}"
        f"{str(bits_sf) + ' bits':>22}"
        f"{economia_sf_texto:>22}"
        f"{taxa_sf:>12.2f}"
        f"{observacao_sf:>22}"
    )

    print(
        f"{'Huffman':<18}"
        f"{str(bits_originais) + ' bits':>22}"
        f"{str(bits_hf) + ' bits':>22}"
        f"{economia_hf_texto:>22}"
        f"{taxa_hf:>12.2f}"
        f"{observacao_hf:>22}"
    )

    print("=" * 120)

    print("\nValidação das descompressões")

    print(f"RLE............. {texto == rle_decodificado}")
    print(f"Shannon-Fano.... {texto == sf_decodificado}")
    print(f"Huffman......... {texto == hf_decodificado}")


def executar_bonus():
    """
    Executa automaticamente os testes utilizando
    os textos fornecidos no enunciado.
    """

    textos = [

        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",

        "BANANABANANABANANABANANA",

        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ]

    print("\n")
    print("=" * 120)
    print("COMPARAÇÃO AUTOMÁTICA DOS TEXTOS DO ENUNCIADO")
    print("=" * 120)

    for i, texto in enumerate(textos, start=1):

        print(f"\nTexto {i}")

        comparar_algoritmos(texto)

    print("\n")
    print("=" * 120)
    print("RESUMO DOS TESTES")
    print("=" * 120)

    print("""
        Texto 1 (repetições consecutivas)
          
        • O Run-Length Encoding apresentou a maior taxa de compressão,
        pois o texto possui longas sequências consecutivas do mesmo símbolo.

        • Shannon-Fano e Huffman também comprimiram o texto
        eficientemente utilizando codificação binária.

        ------------------------------------------------------------

        Texto 2 (repetições não consecutivas)
          
        • Shannon-Fano e Huffman apresentaram excelente desempenho,
        pois exploram a frequência dos símbolos.

        • O Run-Length Encoding não foi eficiente devido à ausência
        de grandes sequências consecutivas.

        ------------------------------------------------------------

        Texto 3 (sem repetições)
          
        • Shannon-Fano e Huffman mantiveram uma boa taxa de compressão.

        • O Run-Length Encoding aumentou o tamanho do texto,
        já que praticamente não existem repetições consecutivas.
    """)


def main():
    """
    Programa principal.
    """

    print("=" * 120)
    print("COMPRESSÃO SEM PERDAS")
    print("Run-Length Encoding (RLE)")
    print("Shannon-Fano")
    print("Huffman")
    print("=" * 120)

    # Primeiro executa os testes do enunciado
    executar_bonus()

    # Depois permite que o usuário faça testes
    while True:

        resposta = input(
            "\nDeseja testar outro texto? (S/N): "
        ).strip().upper()

        if resposta == "N":
            print("\nPrograma encerrado.")
            break

        if resposta != "S":
            print("Opção inválida.")
            continue

        texto = input("\nDigite um texto:\n")

        comparar_algoritmos(texto)


if __name__ == "__main__":
    main()