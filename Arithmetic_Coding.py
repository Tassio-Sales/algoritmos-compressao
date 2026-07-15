from collections import Counter
from fractions import Fraction
import math

def calcular_frequencias(texto):
    """
    Calcula a frequência de cada símbolo presente no texto.

    Parâmetros:
        texto (str): Texto de entrada.

    Retorna:
        dict: Frequência de cada símbolo.
    """

    return dict(sorted(Counter(texto).items()))


def calcular_intervalos(frequencias):
    """
    Constrói os intervalos acumulados de cada símbolo.

    Cada símbolo recebe um intervalo no formato:

        símbolo -> (limite_inferior, limite_superior)

    utilizando frações exatas.

    Parâmetros:
        frequencias (dict): Frequência de cada símbolo.

    Retorna:
        dict: Intervalos acumulados.
    """

    total = sum(frequencias.values())

    intervalos = {}

    acumulado = Fraction(0, 1)

    for simbolo, frequencia in frequencias.items():

        inferior = acumulado

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

    low = Fraction(0, 1)

    high = Fraction(1, 1)

    for simbolo in texto:

        largura = high - low

        inferior, superior = intervalos[simbolo]

        novo_low = low + largura * inferior

        novo_high = low + largura * superior

        low = novo_low

        high = novo_high

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

        valor_normalizado = (
            valor_codificado - low
        ) / largura

        for simbolo, (inferior, superior) in intervalos.items():

            if inferior <= valor_normalizado < superior:

                texto.append(simbolo)

                novo_low = low + largura * inferior
                novo_high = low + largura * superior

                low = novo_low
                high = novo_high

                break

    return "".join(texto)


def estimar_bits(intervalo_final):
    """
    Estima o número mínimo de bits necessários
    para representar o intervalo final.

    Parâmetros:
        intervalo_final (tuple)

    Retorna:
        int
    """

    low, high = intervalo_final

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
    Exibe os intervalos acumulados.
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
    Programa principal.
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