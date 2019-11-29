from simplex import Simplex
from fractions import Fraction
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
            custos[i-1][j-1] = round(Haversine(farm[i-1][1],farm[i-1][2],sol[j-1][1],sol[j-1][2]))
    return custos
'''
def MontaRestricoesLinhas(table, farmacias):
    c = 1
    restlinhas = []
    for a in range(len(table)):
        rest = ""
        for b in range(len(table[0])):
            if(b == 0):
                rest += "1x_" + str(c)
                c = c + 1
            else:
                rest += " + " + "1x_" + str(c)
                c = c + 1
        rest += " <= " + str(int(farmacias[a][3]))
        restlinhas.append(rest)
    return restlinhas

def MontaRestricoesColunas(table, solicitacoes):
    c = 1
    restcol = []
    for b in range(len(table[0])):
        rest = ""
        nc = c
        for a in range(len(table)):
            if(a == 0):
                rest += "1x_" + str(nc)
                nc = nc + len(table[0])
            else:
                rest += " + " + "1x_" + str(nc)
                nc = nc + len(table[0])
        rest += " = " + str(int(solicitacoes[b][3]))
        restcol.append(rest)
        c = c + 1
    return restcol
'''

def MontaRestricoesLinhas(table, farmacias):
    c = 1
    restlinhas = []
    for a in range(len(table)):
        rest = ""
        for b in range(len(table[0])):
            if(b==0):
                rest += "1x_" + str(c)
            else:
                rest += " + 1x_" + str(c)
            c += 1
        if(c-len(table[0]) > 0): #caso linha 1
            for f in range(c):
                rest += " + 0x_" + str(f)
        for f in range(c,len(table)):
            rest += " + 0x_" + str(f+1)

        rest += " <= " + str(int(farmacias[a][3]))
        restlinhas.append(rest)
    return restlinhas

def MontaRestricoesColunas(table, solicitacoes):
    c = 1
    restcol = []
    for b in range(len(table[0])):
        rest = ""
        nc = c
        for a in range(len(table)):
            if(a == 0):
                rest += "1x_" + str(nc)
                nc = nc + len(table[0])
            else:
                rest += " + " + "1x_" + str(nc)
                nc = nc + len(table[0])
        rest += " = " + str(int(solicitacoes[b][3]))
        restcol.append(rest)
        c = c + 1
    return restcol

def MontaObjetivo(table):
    c = 1
    rest = ""
    for a in range(len(table)):
        for b in range(len(table[0])):
            if(a == 0 and b == 0):
                rest += str(int(table[a][b])) + "x_" + str(c)
                c = c + 1
            else:
                rest += " + " + str(int(table[a][b])) + "x_" + str(c)
                c = c + 1
    return rest

def MontaRestricaoUnicidade(table):
    uni = []
    for a in range(len(table)*len(table[0])):
        rest = "1x_"+str(a+1)
        for b in range(len(table)*len(table[0])):
            if(a != b):
                rest += " + 0x_"+str(b+1)
        rest += " >= 0"
        uni.append(rest)
    return uni

## Leitura das coordenadas das lojas, estoque e solicitacoes
farmacias = np.loadtxt('t_farm.csv', delimiter=",", unpack=False, dtype='float')
solicitacoes = np.loadtxt('t_sol.csv', delimiter=",", unpack=False, dtype='float')

## Calculo dos Custos
tablecustos = CalculaDistancias(farmacias, solicitacoes)
print(tablecustos)
l = MontaRestricoesLinhas(tablecustos, farmacias)
print(l[0])
c = MontaRestricoesColunas(tablecustos, solicitacoes)
#print(c)
o = MontaObjetivo(tablecustos)
#print(o)
u = MontaRestricaoUnicidade(tablecustos)
#print(u)

quantvars = len(tablecustos) * len(tablecustos[0])

#print("Quantidade de Variaveis: ", quantvars)
'''
## Texte metodo Simplex
objective = ('min', o)
constraints = l + c 
Lp_system = Simplex(num_vars=quantvars, constraints=constraints, objective_function=objective)
solucao = Lp_system.solution

for r in solucao:
    if r[1] != 0:
        print(r[0] + " -> " + str(r[1]))

print("Custo Total: " + str(Lp_system.optimize_val))
'''
