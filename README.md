# Algoritmos de Compressão Sem Perdas

Projeto desenvolvido para a disciplina de **Sistemas Multimídia** da Universidade Estadual da Paraíba (UEPB).

O objetivo é implementar e comparar algoritmos clássicos de compressão de dados **sem perdas**, analisando suas características, funcionamento e desempenho em diferentes tipos de texto.

Algoritmos implementados:

- Run-Length Encoding (RLE)
- Shannon-Fano
- Huffman
- Huffman Adaptativo
- LZW
- Arithmetic Coding


---

# Algoritmos Implementados


## Run-Length Encoding (RLE)

Algoritmo baseado na substituição de sequências consecutivas de símbolos por sua quantidade de repetições.

Exemplo:

Entrada:AAAAABBBCC

Saída: 5A3B2C

É eficiente principalmente em dados que possuem grandes sequências repetidas.


---

## Shannon-Fano

Algoritmo de compressão estatística baseado na frequência dos símbolos.

Funcionamento:

1. Calcula a frequência dos símbolos.
2. Ordena os símbolos pela frequência.
3. Divide os símbolos em grupos com frequências próximas.
4. Define códigos binários para cada grupo.


A ideia principal é atribuir códigos menores para símbolos mais frequentes.


---

## Huffman

Algoritmo de compressão baseado na construção de uma árvore binária.

Funcionamento:

1. Calcula a frequência dos símbolos.
2. Cria uma fila de prioridade.
3. Combina os símbolos menos frequentes.
4. Constrói a árvore de Huffman.
5. Gera códigos binários menores para símbolos frequentes.


É um dos algoritmos de compressão sem perdas mais utilizados.


---

## Huffman Adaptativo

Versão dinâmica do algoritmo de Huffman que não necessita conhecer previamente as frequências dos símbolos.

O algoritmo constrói e modifica a árvore durante a leitura do texto.

Funcionamento:

1. Inicializa a árvore contendo apenas o nó NYT (Not Yet Transmitted).
2. Para símbolos novos:
   - transmite o código do NYT;
   - envia o símbolo em representação ASCII;
   - insere o novo símbolo na árvore.
3. Para símbolos já conhecidos:
   - utiliza o código atual do símbolo;
   - atualiza os pesos da árvore.
4. Realiza trocas de nós utilizando a estratégia FGK para manter a árvore adaptada.


A principal vantagem é permitir compressão em fluxo de dados, sem uma etapa inicial de análise das frequências.


---

## LZW

Algoritmo baseado na criação dinâmica de um dicionário de sequências.

Funcionamento:

1. Inicializa um dicionário com símbolos individuais.
2. Identifica novas sequências durante a leitura.
3. Adiciona essas sequências ao dicionário.
4. Substitui sequências repetidas por códigos menores.


É utilizado em formatos como GIF e alguns métodos de compressão de arquivos.


---

## Arithmetic Coding

Algoritmo estatístico que representa uma sequência inteira de símbolos através de um intervalo numérico.

Funcionamento:

1. Calcula a frequência dos símbolos.
2. Define probabilidades para cada símbolo.
3. Divide progressivamente o intervalo de representação.
4. Escolhe um valor final dentro do intervalo obtido.


Diferente dos algoritmos baseados em códigos individuais, representa todo o conjunto de dados como uma única sequência numérica.


---

# Comparação dos Algoritmos

O programa: `Comparacao\_Algoritmo.py` executa:

- Testes automáticos fornecidos pelo enunciado.
- Testes personalizados inseridos pelo usuário.
- Comparação da taxa de compressão.
- Cálculo da economia obtida.
- Classificação do desempenho.
- Validação das descompressões.


---

# Execução

Execute:

```bash
python Comparacao_Algoritmo.py

Estrutura do Projeto

.
├── Huffman.py
├── Shannon_Fano.py
├── Run_Length_Encoding.py
├── Adaptive_Huffman.py
├── LZW.py
├── Arithmetic_Coding.py
├── Comparacao_Algoritmo.py
└── README.md



Tecnologias

Python 3
Estruturas de dados
Árvores binárias
Árvores adaptativas
Filas de prioridade
Algoritmos de compressão sem perdas

