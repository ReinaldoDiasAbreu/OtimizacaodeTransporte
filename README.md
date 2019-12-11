# Otimização de Transporte
Aplicação em python com uso do método simplex para otimizar entregas de uma rede de farmácias.

## Objetivo
Desenvolver um programa com o fim de aplicar uma modelagem para minimização do custo de entregas entre farmácias e clientes. Foi considerado como custo a distância entre as lojas e os destinos, para assim determinar quais estabelecimentos devem fazer a entrega a um certo cliente de modo a minimizar o custo, levando em consideração o estoque de cada loja e a quantidade requisitada em cada pedido.

## Modelagem e Aplicação
Esta é a modelagem que minimiza o custo de transporte, e que será usada no método simplex:

![](img/mod_transporte.png)

Este algoritmo, necessita de dois aquivos .csv, que são os arquivos "farmacias.csv" e "solicitacoes.csv", ambos contém um índice, latitude, longitude e estoque ou demanda, separados por vírgula. Como no exemplo:

- "farmacias.csv"

| Loja | Latitude | Longitude | Estoque |
|------|----------|-----------|---------|
|1    | -16.713938 | -43.853936 | 50 |   
|2    | -16.740162 | -43.861820 | 50  | 
|3    | -16.740076 | -43.870815 | 50  |


- "solicitacoes.csv"

| Cliente | Latitude | Longitude | Solicitação |
|------|----------|-----------|---------|
|1    | -16.698133 | -43.869378 | 5     |
|2    | -16.707669 | -43.865173 | 45     |
|3    | -16.694737 | -43.843540 | 100  |


Ao lêr os arquivos, armazena as coordenadas e calcula a distância entre todas as lojas para cada solicitação utilizando a Fórmula de Haversine, que é uma importante equação usada em navegação, fornecendo distâncias entre dois pontos no globo a partir de suas latitudes e longitudes, estas serão o custo de transporte de cada loja para os clientes.

- Tabela do Problema Inicial

| Lojas | S1 | S2 | S3 | Estoque |
|------|----------|-----------|---------|---------|
|L1          | 2  | 1  | 2   | 50     | 
|L2          | 5  | 4  | 5   | 50      |
|L3          | 5  | 4  | 6   | 50      |
|Solicitação | 5  | 45 | 100 |    ---    |


Com esses dados obtemos a função objetivo e restrições:

Z = 2x1 + 1x2+ 2x3 + 5x4 + 4x5 + 5x6 + 5x7 + 4x8 + 6x9

Sujeito a:

x1 + x2 + x3 <= 50

x4 + x5 + x6 <= 50

x7 + x8 + x9 <= 50

x1 + x4 + x7 = 5

x2 + x6 + x8 = 45

x3 + x7 + x9 = 100

x1, x2, x3, x4, x5, x6, x7, x8, x9 >= 0

A partir dessas funções, organizamo-as para que pudessem ser passadas para o algoritmo Simplex Solver, desenvolvido por Michael Stott, em seu repositório no Github citado abaixo, realizamos a alteração desse algoritmo para que atendesse as nossas necessidades.

Por final o algoritmo retorna na tela a solução e gera um arquivo .tex que pode ser compilado com o compilador latex de preferência, e assim obter o relatório em PDF.  

- Solução para o exemplo acima

| Loja | Quant. | Cliente |
|------|--------|---------|
|1    |5     | 1      |
|1    | 45    | 2       |
|2    | 50    | 3       |
|3    | 50    | 3       |
| |
|Custo Total:|14.0 Km|
|Número de Farmácias:|3|
|Número de Clientes:|3|

Caso o problema seja desbalanceado, é indicada uma mensagem informando a quantidade de excesso ou falta de estoque na operação.


## Execução

Para execução desse algoritmo, é necessesário o python (v. 3.7.5) ou superior instalada, e o numpy (v. 1.17.4) e se preferir instale um compilador de códigos latex de sua preferência, ou pode utilizar um compilador de arquivos latex (.tex) online, indicamos o seguinte site:
[LatexBase](https://latexbase.com)

Para execução utilize o sequinte comando no diretório do algoritmo pelo terminal:

```

python3 otimiza.py <csv_fornecimento> <csv_destinos>

```

Especificando os dois arquivos csv correspondentes as lojas e aos clientes, conforme exemplificado anteriormente.

## Desenvolvedores

- [Mirrális Dias Santana](https://github.com/MirrasHue) - Graduando em Ciência da Computação - IFNMG - Montes Claros/MG

- [Reinaldo Junio Dias de Abreu](https://github.com/ReinaldoDiasAbreu) - Graduando em Ciência da Computação - IFNMG - Montes Claros/MG

Aplicação desenvolvida como trabalho de conclusão para disciplina de Pesquisa Operacional, ministrada pela professora [Luciana Balieiro Cosme](https://github.com/lucianaa/).

## Créditos

 - Implementação em Python do Método Simplex: Disponível em: [SimplexSolver](https://github.com/MichaelStott/SimplexSolver)

