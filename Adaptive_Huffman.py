# ============================
# Classes
# ============================

class NoHuffmanAdaptativo:
    """
    Representa um nó da árvore do algoritmo Huffman Adaptativo.

    Um nó pode representar:

        • um símbolo já conhecido pelo algoritmo (folha);

        • um nó interno da árvore;

        • ou o nó NYT (Not Yet Transmitted), utilizado quando um
          símbolo aparece pela primeira vez durante a compressão.

    Atributos:
        simbolo (str):
            Símbolo armazenado no nó.
            None representa o nó NYT ou um nó interno.

        peso (int):
            Quantidade de ocorrências do símbolo ou soma dos pesos
            dos filhos.

        esquerda:
            Filho esquerdo.

        direita:
            Filho direito.

        pai:
            Referência para o nó pai.

        ordem (int):
            Número de ordem utilizado pelo algoritmo FGK para manter
            a estrutura correta da árvore durante as atualizações.
    """

    def __init__(self, simbolo=None, peso=0, ordem=0):

        self.simbolo = simbolo

        self.peso = peso

        self.esquerda = None

        self.direita = None

        self.pai = None

        self.ordem = ordem


    def eh_folha(self):
        """
        Verifica se o nó é uma folha.

        Um nó folha é aquele que não possui filhos,
        representando um símbolo do texto ou o nó NYT.

        Retorna:
            bool
        """

        return (
            self.esquerda is None and
            self.direita is None
        )


    def eh_nyt(self):
        """
        Verifica se o nó representa o NYT
        (Not Yet Transmitted).

        O NYT é um nó folha especial utilizado para
        representar símbolos que ainda não apareceram
        durante a compressão.

        Retorna:
            bool
        """

        return (
            self.eh_folha()
            and
            self.simbolo is None
        )
    
class ArvoreAdaptive:
    """
    Representa a árvore utilizada pelo algoritmo
    Huffman Adaptativo.

    A árvore mantém uma referência para:

        • a raiz;

        • o nó NYT atual;

        • o próximo número de ordem disponível para
        novos nós.
    """

    def __init__(self):

        self.raiz = criar_arvore_inicial()

        self.nyt = self.raiz

        self.proxima_ordem = 512   

# ============================
# Construção inicial
# ============================

def criar_arvore_inicial():
    """
    Cria a árvore inicial do Huffman Adaptativo.

    No início da compressão a árvore contém
    apenas o nó NYT. Pois, nenhum símbolo foi processado ainda.

    Estrutura inicial:

            NYT

    Retorna:
        NoHuffmanAdaptativo:
            Nó raiz da árvore.
    """

    raiz = NoHuffmanAdaptativo(
        simbolo=None,
        peso=0,
        ordem=512
    )

    return raiz

# ============================
# Busca e navegação
# ============================

def buscar_no(no, simbolo):
    """
    Procura recursivamente um símbolo na árvore.

    A busca é realizada em profundidade (DFS),
    percorrendo primeiro a subárvore esquerda e,
    em seguida, a direita.

    Parâmetros:
        no (NoAdaptive): Nó atual.
        simbolo (str): Símbolo procurado.

    Retorna:
        NoAdaptive ou None.
    """

    if no is None:
        return None

    if no.simbolo == simbolo:
        return no

    encontrado = buscar_no(
        no.esquerda,
        simbolo
    )

    if encontrado is not None:
        return encontrado

    return buscar_no(
        no.direita,
        simbolo
    )

def listar_nos(no, lista=None):
    """
    Percorre toda a árvore e retorna uma lista
    contendo todos os nós.

    Essa lista é utilizada posteriormente pelo
    algoritmo FGK para localizar candidatos às
    trocas de posição.

    Parâmetros:
        no (NoHuffmanAdaptativo)

        lista (list):
            Utilizada na recursão.

    Retorna:
        list
    """

    if lista is None:
        lista = []

    if no is None:
        return lista

    lista.append(no)

    listar_nos(
        no.esquerda,
        lista
    )

    listar_nos(
        no.direita,
        lista
    )

    return lista

def eh_ancestral(ancestral, no):
    """
    Verifica se um nó é ancestral de outro.

    A verificação é necessária para impedir trocas
    inválidas durante a atualização da árvore,
    evitando que um nó seja trocado com um de seus
    próprios descendentes.

    Parâmetros:
        ancestral:
            Nó que pode ser ancestral.

        no:
            Nó que será analisado.

    Retorna:
        bool
    """

    atual = no

    while atual is not None:

        if atual == ancestral:
            return True

        atual = atual.pai

    return False

# ============================
# Operações FGK
# ============================

def encontrar_maior_ordem(raiz, peso, ignorar):
    """
    Procura o nó de maior ordem que possui
    o mesmo peso.

    Segundo o algoritmo FGK, cada nó deve ser
    trocado com o líder do bloco de mesmo peso,
    isto é, o nó de maior número de ordem.

    Parâmetros:
        raiz:
            Raiz da árvore.

        peso:
            Peso procurado.

        ignorar:
            Nó que não pode ser retornado.

    Retorna:
        NoHuffmanAdaptativo ou None.
    """

    lista = []

    listar_nos(
        raiz,
        lista
    )

    candidato = None

    for no in lista:

        if no == ignorar:
            continue

        if no.peso != peso:
            continue

        if (
            candidato is None
            or
            no.ordem > candidato.ordem
        ):
            candidato = no

    return candidato

def encontrar_no_para_troca(raiz, no):
    """
    Determina se existe um nó que pode ser trocado
    com o nó atual durante a atualização FGK.

    O candidato deve:

        • possuir o mesmo peso;

        • ter maior número de ordem;

        • não ser ancestral nem descendente do nó
        atual.

    Retorna:
        NoHuffmanAdaptativo ou None.
    """

    candidato = encontrar_maior_ordem(
        raiz,
        no.peso,
        no
    )

    if candidato is None:
        return None

    if candidato == no:
        return None

    if eh_ancestral(no, candidato):
        return None

    if eh_ancestral(candidato, no):
        return None

    return candidato

def trocar_nos(no1, no2):
    """
    Troca a posição de dois nós na árvore.

    Apenas os ponteiros dos pais são
    atualizados.    

    A troca altera apenas as referências para os
    pais dos nós e seus respectivos números de
    ordem. Os filhos permanecem inalterados.

    Essa operação preserva a estrutura das
    subárvores.

    Parâmetros:
        no1
        no2
    """

    if (
        no1 is None or
        no2 is None or
        no1 == no2
    ):
        return

    pai1 = no1.pai
    pai2 = no2.pai

    if pai1 is None or pai2 is None:
        return

    if pai1.esquerda == no1:
        pai1.esquerda = no2
    else:
        pai1.direita = no2

    if pai2.esquerda == no2:
        pai2.esquerda = no1
    else:
        pai2.direita = no1

    no1.pai = pai2
    no2.pai = pai1

    no1.ordem, no2.ordem = (
        no2.ordem,
        no1.ordem
    )

def atualizar_arvore(raiz, no):
    """
    Atualiza a árvore seguindo a ideia do
    algoritmo FGK.

    Para cada nó até a raiz:

        1. procura um nó de mesmo peso
           com maior número de ordem;

        2. caso exista, realiza a troca;

        3. incrementa o peso;

        4. sobe para o pai.
        
    Esse processo garante que a árvore continue
    obedecendo às propriedades do algoritmo FGK
    após o processamento de cada símbolo.
    """

    atual = no

    # Percorre do nó modificado até a raiz, atualizando toda a árvore.
    while atual is not None:        

        candidato = encontrar_no_para_troca(
            raiz,
            atual
        )

        # Caso exista um líder do bloco válido, realiza a troca de posições.
        if candidato is not None:

            trocar_nos(
                atual,
                candidato
            )

        # Atualiza o peso do nó após o processamento do símbolo.
        atual.peso += 1

        # Continua a atualização no nó pai.
        atual = atual.pai

# ============================
# Operações auxiliares
# ============================

def obter_codigo(no):
    """
    Obtém o código binário correspondente
    ao caminho da raiz até o nó informado.

    Como cada nó possui apenas uma referência para
    o pai, o percurso é realizado do nó até a raiz,
    sendo o código invertido ao final.

    Convenção:

        esquerda -> 0
        direita  -> 1

    Parâmetros:
        no (NoHuffmanAdaptativo)

    Retorna:
        str:
            Código binário do símbolo.
    """

    codigo = []

    atual = no

    # Percorre dos nós folha até a raiz.
    while atual.pai is not None:

        if atual == atual.pai.esquerda:

            codigo.append("0")

        else:

            codigo.append("1")

        atual = atual.pai
    
    # O percurso foi construído de trás para frente, portanto o código precisa ser invertido.
    codigo.reverse()

    return "".join(codigo)

def ascii_8_bits(simbolo):
    """
    Converte um caractere para sua representação
    ASCII utilizando exatamente 8 bits.

    Essa representação é utilizada quando um
    símbolo aparece pela primeira vez durante
    a compressão.

    Parâmetros:
        simbolo (str)

    Retorna:
        str:
            Representação binária em 8 bits.
    """

    return format(
        ord(simbolo),
        "08b"
    )

def decodificar_simbolo(arvore, bits, indice):
    """
    Decodifica um único símbolo da sequência
    de bits.

    A função percorre a árvore até encontrar
    uma folha.

    Caso a folha seja um nó NYT, os próximos
    8 bits são interpretados como um novo
    caractere ASCII.

    Parâmetros:
        arvore (ArvoreAdaptive)

        bits (str)

        indice (int):
            Posição atual da leitura.

    Retorna:
        tuple:

            (símbolo_decodificado, novo_indice)
    """

    atual = arvore.raiz

    # Percorre a árvore até alcançar uma folha.
    while not atual.eh_folha():

        if indice >= len(bits):
            raise ValueError(
                "Sequência de bits inválida."
            )

        if bits[indice] == "0":

            atual = atual.esquerda

        elif bits[indice] == "1":

            atual = atual.direita

        else:

            raise ValueError(
                "Bit inválido encontrado."
            )

        indice += 1

    # Caso seja o nó NYT, os próximos 8 bits representam um novo símbolo ASCII.
    if atual.eh_nyt():

        if indice + 8 > len(bits):

            raise ValueError(
                "Sequência de bits inválida."
            )


        ascii_bits = bits[
            indice:
            indice + 8
        ]


        simbolo = chr(
            int(ascii_bits, 2)
        )


        indice += 8

    # Símbolo já conhecido pela árvore.
    else:

        simbolo = atual.simbolo


    return (
        simbolo,
        indice
    )

# ============================
# Inserção e atualização
# ============================
    
def inserir_novo_simbolo(nyt, simbolo, proxima_ordem):
    """
    Insere um novo símbolo na árvore.
    O antigo nó NYT passa a ser um nó interno,
    enquanto um novo NYT é criado como filho
    esquerdo.

    O nó NYT deixa de ser folha e passa a possuir
    dois filhos:

        esquerda -> novo NYT
        direita  -> símbolo

    Retorna:
        tuple:
            (novo_no_simbolo, novo_nyt)
    """

    # Cria o novo nó NYT e o novo símbolo, preservando a numeração de ordem.
    novo_nyt = NoHuffmanAdaptativo(
        simbolo=None,
        peso=0,
        ordem=proxima_ordem - 2
    )

    novo_simbolo = NoHuffmanAdaptativo(
        simbolo=simbolo,
        peso=0,
        ordem=proxima_ordem - 1
    )

    nyt.esquerda = novo_nyt
    nyt.direita = novo_simbolo

    novo_nyt.pai = nyt
    novo_simbolo.pai = nyt

    nyt.simbolo = None
    nyt.peso = 0

    return (
        novo_simbolo,
        novo_nyt
    )

def inserir_simbolo(arvore, simbolo):
    """
    Processa um símbolo durante a compressão.

    Essa função representa a principal etapa da
    compressão adaptativa, pois decide se o
    símbolo já faz parte da árvore ou se deve
    ser inserido pela primeira vez.

    Se o símbolo já existir na árvore:

        • emite seu código atual;
        • atualiza a árvore.

    Caso contrário:

        • emite o código do NYT;
        • emite o ASCII (8 bits) do símbolo;
        • insere o símbolo na árvore;
        • atualiza a árvore.

    Parâmetros:
        arvore (ArvoreAdaptive)

        simbolo (str)

    Retorna:
        str:
            Sequência de bits produzida.
    """

    # Procura o símbolo na árvore atual.
    no = buscar_no(
        arvore.raiz,
        simbolo
    )

    # -----------------------------------
    # Símbolo já conhecido
    # -----------------------------------

    if no is not None:

        codigo = obter_codigo(
            no
        )

        atualizar_arvore(
            arvore.raiz,
            no
        )

        # Retorna apenas o código do símbolo, pois ele já está presente na árvore.
        return codigo

    # -----------------------------------
    # Novo símbolo
    # -----------------------------------

    codigo_nyt = obter_codigo(
        arvore.nyt
    )

    codigo_ascii = ascii_8_bits(
        simbolo
    )

    # O novo símbolo passa a ocupar a posição à direita do antigo nó NYT.
    novo_no, novo_nyt = inserir_novo_simbolo(
        arvore.nyt,
        simbolo,
        arvore.proxima_ordem
    )

    arvore.nyt = novo_nyt

    arvore.proxima_ordem -= 2

    # Atualiza a árvore após a inserção do símbolo.
    atualizar_arvore(
        arvore.raiz,
        novo_no
    )

    return (
        codigo_nyt
        +
        codigo_ascii
    )

def atualizar_simbolo_decodificado(arvore, simbolo):
    """
    Atualiza a árvore durante a decodificação.

    Após recuperar um símbolo da sequência de bits,
    a árvore precisa sofrer exatamente as mesmas
    modificações realizadas durante a compressão,
    garantindo que codificador e decodificador
    permaneçam sincronizados.

    Parâmetros:
        arvore (ArvoreAdaptive)

        simbolo (str)
    """

    # Verifica se o símbolo já existe na árvore.
    no = buscar_no(
        arvore.raiz,
        simbolo
    )

    if no is not None:

        atualizar_arvore(
            arvore.raiz,
            no
        )

        return

    # O símbolo ainda não existe: cria um novo nó e atualiza a árvore.
    novo_no, novo_nyt = inserir_novo_simbolo(
        arvore.nyt,
        simbolo,
        arvore.proxima_ordem
    )

    arvore.nyt = novo_nyt

    arvore.proxima_ordem -= 2

    atualizar_arvore(
        arvore.raiz,
        novo_no
    )

# ============================
# Compressão / Descompressão
# ============================

def adaptive_huffman(texto):
    """
    Comprime um texto utilizando o algoritmo
    Huffman Adaptativo.

    Os símbolos são processados um a um e, após
    cada símbolo, a árvore é atualizada conforme
    o algoritmo FGK.

    Parâmetros:
        texto (str):
            Texto original.

    Retorna:
        tuple:

            - str:
                Sequência de bits produzida.

            - ArvoreAdaptive:
                Árvore final após o processamento
                de todo o texto.
    """

    # Inicializa a árvore contendo apenas o nó NYT.
    arvore = ArvoreAdaptive()

    bits_saida = []

    # Processa cada símbolo do texto de forma sequencial.
    for simbolo in texto:

        bits_saida.append(
            inserir_simbolo(
                arvore,
                simbolo
            )
        )

    return (
        "".join(bits_saida),
        arvore
    )

def adaptive_huffman_decode(bits):
    """
    Reconstrói o texto original a partir da sequência
    de bits produzida pelo Huffman Adaptativo.

    Durante a decodificação, a árvore é reconstruída
    dinamicamente da mesma forma que ocorreu na
    compressão, garantindo a sincronização entre
    codificador e decodificador.

    Parâmetros:
        bits (str):
            Sequência de bits comprimida.

    Retorna:
        str:
            Texto reconstruído.
    """

    arvore = ArvoreAdaptive()

    indice = 0

    texto = []

    # Processa todos os bits até reconstruir completamente o texto original.
    while indice < len(bits):

        simbolo, indice = decodificar_simbolo(
            arvore,
            bits,
            indice
        )


        texto.append(simbolo)

        # Atualiza a árvore exatamente como ocorreu durante a compressão.
        atualizar_simbolo_decodificado(
            arvore,
            simbolo
        )


    return "".join(texto)


# ============================
# Testes
# ============================

def imprimir_arvore(no, nivel=0):
    """
    Exibe a árvore em formato hierárquico.

    Função utilizada apenas para visualização e
    depuração do algoritmo, facilitando o entendimento
    da estrutura construída durante a compressão.

    Parâmetros:
        no:
            Nó atual.

        nivel:
            Profundidade do nó na árvore.
    """

    if no is None:
        return

    # Define a indentação de acordo com a profundidade do nó.
    espaco = "   " * nivel

    # Nó NYT.
    if no.eh_nyt():

        print(
            espaco + "NYT"
        )

    # Nó folha contendo um símbolo.
    elif no.simbolo is not None:

        print(
            espaco +
            f"{repr(no.simbolo)} "
            f"(peso={no.peso})"
        )

    # Nó interno.
    else:

        print(
            espaco +
            f"* (peso={no.peso})"
        )


    imprimir_arvore(
        no.esquerda,
        nivel + 1
    )

    imprimir_arvore(
        no.direita,
        nivel + 1
    )

def tamanho_arvore(no):
    """
    Calcula a quantidade de nós da árvore.
    O cálculo é realizado recursivamente,
    percorrendo todos os nós da árvore.

    Parâmetros:
        no:
            Nó raiz.

    Retorna:
        int:
            Número total de nós.
    """

    if no is None:

        return 0

    # Conta o nó atual e todos os nós das subárvores esquerda e direita.
    return (
        1
        +
        tamanho_arvore(no.esquerda)
        +
        tamanho_arvore(no.direita)
    )


def main():
    """
    Executa um exemplo completo do algoritmo
    Huffman Adaptativo.

    O programa realiza:

        - leitura do texto;

        - compressão;

        - descompressão;

        - exibição da sequência de bits;

        - impressão da árvore final;

        - validação da reconstrução.
    """

    texto = input("Digite um texto: ")

    # Compressão
    bits, arvore = adaptive_huffman(
        texto
    )

    # Descompressão
    texto_reconstruido = adaptive_huffman_decode(
        bits
    )

    # Exibição dos resultados
    print("\nBits produzidos:\n")
    print(bits)

    print("\nQuantidade de bits:")
    print(len(bits))

    print("\nTamanho da árvore:")
    print(tamanho_arvore(arvore.raiz))

    print("\nÁrvore Huffman Adaptativa:")
    imprimir_arvore(
        arvore.raiz
    )


    print("\nTexto reconstruído:")
    print(texto_reconstruido)

    print("\nReconstrução correta:")
    print(texto == texto_reconstruido)

if __name__ == "__main__":
    main()