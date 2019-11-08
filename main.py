from simplex import Simplex
from fractions import Fraction
from prettytable import PrettyTable
import numpy as np
import math
import csv

## Funcao para calculo de distancia entre coordenadas em km
def Haversine(lat1, lon1, lat2, lon2): 
    # Distancia entre as coordenadas
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
    # Conversão para radianos
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
    # Aplicando valores a formula
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a)) 
    return rad * c

## Calcula custo da posicao de cada farmacia para as solicitacoes
def CalculaDistancias(farm, sol):
    custos = np.zeros((len(farm),len(sol)))
    for i in range(len(farm)):
        for j in range(len(sol)):
            custos[i-1][j-1] = Haversine(farm[i-1][1],farm[i-1][2],sol[j-1][1],sol[j-1][2])
    return custos

## Leitura das coordenadas das lojas, estoque e solicitacoes
farmacias = np.loadtxt('farmacias.csv', delimiter=",", unpack=False, dtype='float')
solicitacoes = np.loadtxt('solicitacoes.csv', delimiter=",", unpack=False, dtype='float')

## Calculo dos Custos
tablecustos = CalculaDistancias(farmacias, solicitacoes)

## Tabela de Custos
size  = len(tablecustos[0])
h = list(range(size))
x = PrettyTable(h)
for i in tablecustos:
    row = i
    x.add_row(row) 
print(x)

## Texte metodo Simplex
objective = ('maximize', '2x_1 + 7x_2')
constraints = ['3x_1 + 2x_2 >= 20', '4x_1 + 4x_2 <= 32']
Lp_system = Simplex(num_vars=2, constraints=constraints, objective_function=objective)
print(Lp_system.solution)
print(Lp_system.optimize_val)
