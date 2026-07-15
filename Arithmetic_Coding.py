from collections import Counter
from fractions import Fraction
import math


def calcular_frequencias(texto):
    """
    Calcula a frequência de ocorrência de cada símbolo.

    Os símbolos são armazenados em ordem crescente para que
    compressor e descompressor construam exatamente os mesmos
    intervalos acumulados.

    Parâmetros:
        texto (str):
            Texto de entrada.

    Retorna:
        dict:
            Frequência de cada símbolo.
    """

    return dict(sorted(Counter(texto).items()))


def calcular_intervalos(frequencias):
    """
    Constrói os intervalos acumulados de cada símbolo.

    Cada símbolo recebe um intervalo no formato:

        símbolo -> (limite_inferior, limite_superior)

    utilizando frações exatas.

    Os intervalos são construídos de forma acumulativa dentro
    do intervalo [0, 1), sendo proporcionais à frequência
    de cada símbolo.

    Parâmetros:
        frequencias (dict): Frequência de cada símbolo.

    Retorna:
        dict: Intervalos acumulados.
    """

    total = sum(frequencias.values())

    intervalos = {}

    acumulado = Fraction(0, 1)

    for simbolo, frequencia in frequencias.items():

        # O limite inferior corresponde ao ponto onde termina o intervalo do símbolo anterior.
        inferior = acumulado

        # O tamanho do intervalo é proporcional à frequência do símbolo.
        superior = acumulado + Fraction(frequencia, total)

        intervalos[simbolo] = (
            inferior,
            superior
        )

        acumulado = superior

    return intervalos


def arithmetic_coding(texto):
    """
    Realiza a compressão utilizando Codificação Aritmética.

    Parâmetros:
        texto (str): Texto de entrada.

    Retorna:
        tuple contendo:

            valor_codificado (Fraction)
            intervalo_final (tuple)
            frequencias (dict)
            intervalos (dict)
    """

    if not texto:

        return (
            Fraction(0, 1),
            (Fraction(0, 1), Fraction(1, 1)),
            {},
            {}
        )

    frequencias = calcular_frequencias(texto)

    intervalos = calcular_intervalos(frequencias)

    # Inicialmente todo o intervalo [0,1) representa qualquer mensagem possível.
    low = Fraction(0, 1)

    high = Fraction(1, 1)

    for simbolo in texto:

        # Calcula a largura do intervalo atual.
        largura = high - low

        # Obtém o subintervalo correspondente ao símbolo atual.
        inferior, superior = intervalos[simbolo]

        # Reduz o intervalo atual para o subintervalo correspondente ao símbolo.
        novo_low = low + largura * inferior

        novo_high = low + largura * superior

        low = novo_low

        high = novo_high

    # Qualquer valor dentro do intervalo final representa corretamente toda a mensagem.
    # Aqui é utilizado o ponto médio.
    valor_codificado = (low + high) / 2

    return (
        valor_codificado,
        (low, high),
        frequencias,
        intervalos
    )

def arithmetic_decode(valor_codificado, frequencias, tamanho_texto):
    """
    Reconstrói o texto original a partir do valor codificado.
    Durante a reconstrução, o intervalo é reduzido da mesma
    forma utilizada na compressão, permitindo recuperar um
    símbolo por vez.

    Parâmetros:
        valor_codificado (Fraction): Valor obtido na compressão.
        frequencias (dict): Frequência dos símbolos.
        tamanho_texto (int): Quantidade de símbolos do texto original.

    Retorna:
        str: Texto reconstruído.
    """

    if tamanho_texto == 0:
        return ""

    intervalos = calcular_intervalos(frequencias)

    low = Fraction(0, 1)
    high = Fraction(1, 1)

    texto = []

    for _ in range(tamanho_texto):

        largura = high - low

        # Reposiciona o valor codificado para o intervalo [0,1), facilitando a busca pelo próximo símbolo.
        valor_normalizado = (
            valor_codificado - low
        ) / largura

        # Procura o intervalo que contém o valor normalizado.
        for simbolo, (inferior, superior) in intervalos.items():

            if inferior <= valor_normalizado < superior:

                texto.append(simbolo)
                
                novo_low = low + largura * inferior
                novo_high = low + largura * superior

                # Atualiza o intervalo para continuar a reconstrução do próximo símbolo.
                low = novo_low
                high = novo_high

                break

    return "".join(texto)


def estimar_bits(intervalo_final):
    """
    Estima quantos bits seriam necessários para representar
    qualquer valor pertencente ao intervalo final.

    Essa estimativa é utilizada apenas para comparação com
    os demais algoritmos e não corresponde exatamente à
    representação utilizada por implementações completas da
    Codificação Aritmética.

    Parâmetros:
        intervalo_final (tuple)

    Retorna:
        int
    """

    low, high = intervalo_final
    
    # Quanto menor o intervalo final, maior será a quantidade de bits necessária para representá-lo.
    largura = high - low

    if largura <= 0:
        return 0

    return math.ceil(
        -math.log2(
            float(largura)
        )
    )

def imprimir_frequencias(frequencias):
    """
    Exibe as frequências dos símbolos.
    """

    print("\n========== FREQUÊNCIAS ==========\n")

    for simbolo, frequencia in frequencias.items():
        
        print(f"{repr(simbolo):>4} -> {frequencia:>3}")


def imprimir_intervalos(intervalos):
    """
    Exibe os intervalos acumulados associados
    a cada símbolo.

    Os valores são apresentados em formato decimal
    apenas para facilitar a visualização.
    Internamente, o algoritmo utiliza frações exatas.
    """

    print("\n========== INTERVALOS ==========\n")

    for simbolo, (inferior, superior) in intervalos.items():

        print(
            f"{repr(simbolo):>6} -> "
            f"[{float(inferior):.6f}, "
            f"{float(superior):.6f})"
        )
        
def main():
    """
    Executa um exemplo completo da Codificação Aritmética.

    O programa realiza:

        - leitura do texto;

        - cálculo das frequências;

        - construção dos intervalos;

        - compressão;

        - reconstrução do texto;

        - exibição do valor codificado;

        - comparação dos tamanhos.
    """

    texto = input("Digite um texto: ")

    (
        valor_codificado,
        intervalo_final,
        frequencias,
        intervalos
    ) = arithmetic_coding(texto)

    texto_reconstruido = arithmetic_decode(
        valor_codificado,
        frequencias,
        len(texto)
    )

    bits_estimados = estimar_bits(
        intervalo_final
    )

    bits_originais = len(texto) * 8

    economia = bits_originais - bits_estimados

    taxa = 0.0

    if bits_originais > 0:

        taxa = (
            economia
            / bits_originais
        ) * 100

    imprimir_frequencias(
        frequencias
    )

    imprimir_intervalos(
        intervalos
    )

    print("\n========== RESULTADOS ==========\n")

    print("Texto original:")
    print(texto)

    print("\n========== CODIFICAÇÃO ==========\n")

    print("Valor representativo (fração exata):")
    print(valor_codificado)

    print("\nValor representativo (decimal):")
    print(f"{float(valor_codificado):.20f}")

    print("\nIntervalo final (decimal):")

    print(
        f"[{float(intervalo_final[0]):.20f}, "
        f"{float(intervalo_final[1]):.20f})"
    )

    # Quanto menor a largura, maior o poder de compressão obtido.
    largura = intervalo_final[1] - intervalo_final[0]

    print("\nLargura do intervalo:")
    print(f"{float(largura):.5e}")
    
    print(
        f"\nBits estimados da representação: {bits_estimados}"
    )

    print("\nTexto reconstruído:")
    print(texto_reconstruido)

    print("\n========== TAMANHOS ==========\n")

    print(
        f"Texto original: {len(texto)} caracteres ({bits_originais} bits)"
    )

    print(
        f"Economia: {economia} bits"
    )

    print(
        f"Taxa de compressão: {taxa:.2f}%"
    )


if __name__ == "__main__":
    main()