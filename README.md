\# Algoritmos de Compressão Sem Perdas



Projeto desenvolvido para a disciplina de Sistemas Multimídia da Universidade Estadual da Paraíba (UEPB).



O objetivo é implementar e comparar algoritmos clássicos de compressão de dados sem perdas:



\- Run-Length Encoding (RLE)

\- Shannon-Fano

\- Huffman





\## Algoritmos Implementados



\### Run-Length Encoding (RLE)



Algoritmo baseado em repetição consecutiva de símbolos.



Exemplo:



Entrada: AAAAABBBCC



Saída: 5A3B2C





É eficiente para dados com grandes sequências repetidas.





\---



\### Shannon-Fano



Algoritmo de compressão estatística baseado na frequência dos símbolos.



Processo:



1\. Calcula a frequência dos símbolos.

2\. Ordena os símbolos pela frequência.

3\. Divide os símbolos em grupos com frequências próximas.

4\. Define códigos binários para cada grupo.





\---



\### Huffman



Algoritmo de compressão baseado em árvore binária.



Processo:



1\. Calcula a frequência dos símbolos.

2\. Cria uma fila de prioridade.

3\. Combina os símbolos menos frequentes.

4\. Constrói a árvore de Huffman.

5\. Gera códigos binários menores para símbolos frequentes.





\## Comparação dos Algoritmos



O programa `Comparacao\_Algoritmo.py` executa:



\- Testes automáticos fornecidos pelo enunciado.

\- Testes personalizados inseridos pelo usuário.

\- Comparação da taxa de compressão.

\- Validação da descompressão.





\## Execução



Execute:



```bash

python Comparacao\_Algoritmo.py



Estrutura do Projeto

.

├── Huffman.py

├── Shannon\_Fano.py

├── Run\_Length\_Encoding.py

├── Comparacao\_Algoritmo.py

└── README.md



Tecnologias



Python 3

Estruturas de dados

Árvores binárias

Filas de prioridade

Algoritmos de compressão

