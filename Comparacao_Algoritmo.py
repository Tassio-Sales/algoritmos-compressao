import math
from Run_Length_Encoding import rle, rle_decode
from Shannon_Fano import shannon_fano, shannon_fano_decode
from Huffman import huffman, huffman_decode
from LZW import lzw, lzw_decode
from Arithmetic_Coding import arithmetic_coding, arithmetic_decode, estimar_bits
from Adaptive_Huffman import adaptive_huffman, adaptive_huffman_decode


LARGURA_TABELA = 140


def calcular_taxa_compressao(tamanho_original, tamanho_comprimido):
    """
    Calcula a taxa de compressão obtida por um algoritmo.

    A taxa corresponde ao percentual de redução do tamanho
    original após a compressão.

    Fórmula utilizada:

        taxa = (1 - comprimido/original) × 100

    Parâmetros:
        tamanho_original (int):
            Tamanho do texto original.

        tamanho_comprimido (int):
            Tamanho da representação comprimida.

    Retorna:
        float:
            Percentual de compressão obtido.
    """

    if tamanho_original == 0:
        return 0.0

    return (1 - (tamanho_comprimido / tamanho_original)) * 100

def classificar_desempenho(taxa):
    """
    Classifica qualitativamente a taxa de compressão.

    A classificação é utilizada apenas para facilitar
    a interpretação dos resultados apresentados na tabela.

    Parâmetros:
        taxa (float):
            Taxa de compressão em porcentagem.

    Retorna:
        str:
            Classificação do desempenho.
    """

    if taxa >= 80:
        return "Excelente"

    if taxa >= 40:
        return "Bom"

    if taxa >= 20:
        return "Regular"

    return "Pouco eficiente"

def comparar_algoritmos(texto):
    """
    Executa todos os algoritmos implementados e compara
    seus resultados para um mesmo texto.

    Para cada algoritmo são calculados:

        - tamanho da representação comprimida;

        - economia obtida;

        - taxa de compressão;

        - classificação do desempenho;

        - validação da descompressão.

    Parâmetros:
        texto (str):
            Texto que será utilizado nos testes.
    """

    print("\n" + "=" * LARGURA_TABELA)
    print("Texto original:")
    print(texto)
    print("=" * LARGURA_TABELA)

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

    economia_hf_texto = f"{economia_hf} bits"

    observacao_hf = classificar_desempenho(taxa_hf)

    # ==========================================================
    # Huffman Adaptativo
    # ==========================================================

    ah_codificado, _ = adaptive_huffman(texto)

    ah_decodificado = adaptive_huffman_decode(
        ah_codificado
    )

    bits_ah = len(ah_codificado)

    taxa_ah = calcular_taxa_compressao(
        bits_originais,
        bits_ah
    )

    economia_ah = bits_originais - bits_ah

    economia_ah_texto = f"{economia_ah} bits"

    observacao_ah = classificar_desempenho(
        taxa_ah
    )

    # ==========================================================
    # LZW
    # ==========================================================

    lzw_codigos, _ = lzw(texto)

    lzw_decodificado = lzw_decode(lzw_codigos)

    if lzw_codigos:
        maior_codigo = max(lzw_codigos)
    else:
        maior_codigo = 255

    bits_por_codigo = max(8,math.ceil(math.log2(maior_codigo + 1)))

    bits_lzw = len(lzw_codigos) * bits_por_codigo

    taxa_lzw = calcular_taxa_compressao(
        bits_originais,
        bits_lzw
    )

    economia_lzw = bits_originais - bits_lzw

    economia_lzw_texto = f"{economia_lzw} bits"

    observacao_lzw = classificar_desempenho(
        taxa_lzw
    )

    # ==========================================================
    # Arithmetic Coding
    # ==========================================================

    (
        valor_codificado,
        intervalo_final,
        frequencias,
        intervalos
    ) = arithmetic_coding(texto)

    arithmetic_decodificado = arithmetic_decode(
        valor_codificado,
        frequencias,
        len(texto)
    )

    bits_arithmetic = estimar_bits(intervalo_final)

    # Garante que pelo menos exista uma representação mínima
    if bits_arithmetic == 0:
        bits_arithmetic = 1

    taxa_arithmetic = calcular_taxa_compressao(
        bits_originais,
        bits_arithmetic
    )

    economia_arithmetic = (
        bits_originais - bits_arithmetic
    )

    economia_arithmetic_texto = (
        f"{economia_arithmetic} bits"
    )

    observacao_arithmetic = (
        classificar_desempenho(
            taxa_arithmetic
        )
    )

    # ==========================================================
    # Exibição da tabela comparativa
    # ==========================================================

    print("\nTabela Comparativa\n")

    print("=" * LARGURA_TABELA)

    print(
    f"{'Algoritmo':<22}"
    f"{'Original':>20}"
    f"{'Comprimido':>20}"
    f"{'Economia obtida':>22}"
    f"{'Taxa (%)':>12}"
    f"{'Observação':>22}"
    )

    print("=" * LARGURA_TABELA)

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

    print(
        f"{'Huffman Adapt.':<18}"
        f"{str(bits_originais) + ' bits':>22}"
        f"{str(bits_ah) + ' bits':>22}"
        f"{economia_ah_texto:>22}"
        f"{taxa_ah:>12.2f}"
        f"{observacao_ah:>22}"
    )

    print(
        f"{'LZW':<18}"
        f"{str(bits_originais) + ' bits':>22}"
        f"{str(bits_lzw) + ' bits':>22}"
        f"{economia_lzw_texto:>22}"
        f"{taxa_lzw:>12.2f}"
        f"{observacao_lzw:>22}"
    )

    print(
        f"{'Arithmetic Coding':<18}"
        f"{str(bits_originais) + ' bits':>22}"
        f"{str(bits_arithmetic) + ' bits':>22}"
        f"{economia_arithmetic_texto:>22}"
        f"{taxa_arithmetic:>12.2f}"
        f"{observacao_arithmetic:>22}"
    )

    print("=" * LARGURA_TABELA)

    # Verifica se todos os algoritmos reconstruíram exatamente o texto original.
    print("\nValidação das descompressões")

    print(f"{'RLE':<18} {texto == rle_decodificado}")
    print(f"{'Shannon-Fano':<18} {texto == sf_decodificado}")
    print(f"{'Huffman':<18} {texto == hf_decodificado}")
    print(f"{'Huffman Adapt.':<18} {texto == ah_decodificado}")
    print(f"{'LZW':<18} {texto == lzw_decodificado}")
    print(f"{'Arithmetic Coding':<18} {texto == arithmetic_decodificado}")

def executar_bonus():
    """
    Executa automaticamente os testes utilizando
    os textos fornecidos no enunciado.

    Ao final, apresenta um resumo explicando
    o comportamento de cada algoritmo em
    diferentes tipos de entrada.
    """

    textos = [

        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",

        "BANANABANANABANANABANANA",

        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ]

    print("\n")
    print("=" * LARGURA_TABELA)
    print("COMPARAÇÃO AUTOMÁTICA DOS TEXTOS DO ENUNCIADO")
    print("=" * LARGURA_TABELA)

    for i, texto in enumerate(textos, start=1):

        print(f"\nTexto {i}")

        comparar_algoritmos(texto)

    print("\n")
    print("=" * LARGURA_TABELA)
    print("RESUMO DOS TESTES")
    print("=" * LARGURA_TABELA)

    print("""
        Texto 1 (repetições consecutivas)       

        • O Run-Length Encoding apresentou excelente desempenho,
        pois o texto possui uma sequência longa de símbolos repetidos,
        sendo uma situação ideal para esse algoritmo.

        • Shannon-Fano e Huffman também obtiveram excelente compressão,
        explorando a alta frequência do único símbolo presente no texto.
        
        • O Huffman Adaptativo apresentou um desempenho ligeiramente inferior
        ao Huffman estático, pois precisou transmitir inicialmente o símbolo
        através do nó NYT antes de aprender sua frequência. Após a adaptação,
        conseguiu explorar eficientemente a repetição do símbolo.

        • O LZW apresentou um bom desempenho,
        aprendendo rapidamente as sequências repetidas e reduzindo
        significativamente o tamanho da mensagem.
        
        • O Arithmetic Coding apresentou a maior taxa estimada,
        porém esse resultado considera apenas a representação matemática
        do intervalo final e não inclui os metadados necessários.

        ------------------------------------------------------------

        Texto 2 (repetições não consecutivas)
        
        • O Run-Length Encoding não foi eficiente,
        pois quase não existem repetições consecutivas de caracteres.
          
        • Shannon-Fano e Huffman apresentaram o melhor desempenho,
        pois utilizam a frequência dos símbolos para gerar códigos menores
        para os caracteres mais recorrentes.
        
        • O Huffman Adaptativo apresentou desempenho inferior ao Huffman
        estático neste teste, devido ao custo inicial de inserção dos novos
        símbolos utilizando o nó NYT. 
          
        • O LZW também conseguiu comprimir o texto,
        identificando sequências recorrentes ao longo da mensagem,
        embora com desempenho inferior ao de Shannon-Fano e Huffman.
        
        • O Arithmetic Coding também apresentou excelente desempenho,
        pois utiliza diretamente as probabilidades dos símbolos
        para reduzir o intervalo final de representação.

        ------------------------------------------------------------

        Texto 3 (sem repetições)
        
        • O Run-Length Encoding aumentou o tamanho do texto,
        já que não existem repetições consecutivas de caracteres.
        
        • Shannon-Fano e Huffman ainda conseguiram reduzir
        o tamanho da representação por meio da codificação binária
        baseada na frequência dos símbolos.
        
        • O Huffman Adaptativo apresentou o pior desempenho neste cenário,
        pois todos os símbolos aparecem apenas uma vez. Como consequência,
        o algoritmo precisou transmitir cada novo símbolo utilizando o nó NYT,
        adicionando um custo extra sem conseguir aproveitar repetições.
          
        • O LZW praticamente não obteve compressão,
        pois as sequências adicionadas ao dicionário não voltaram
        a se repetir ao longo da mensagem.
                
        • O Arithmetic Coding apresentou resultado semelhante,
        pois ainda consegue explorar pequenas diferenças de frequência,
        mesmo em textos com poucos padrões repetidos.
        
    """)


def main():
    """
    Programa principal.

    Exibe uma comparação automática utilizando
    os textos do enunciado e, em seguida,
    permite que o usuário realize novos testes
    com textos personalizados.
    """

    print("=" * LARGURA_TABELA)
    print("COMPARAÇÃO DE ALGORITMOS DE COMPRESSÃO SEM PERDAS")
    print("Run-Length Encoding (RLE)")
    print("Shannon-Fano")
    print("Huffman")
    print("Huffman Adaptativo")
    print("LZW")
    print("Arithmetic Coding")
    print("=" * LARGURA_TABELA)

    # Executa automaticamente os testes previstos no enunciado.
    executar_bonus()

    # Permite que o usuário realize testes personalizados.
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