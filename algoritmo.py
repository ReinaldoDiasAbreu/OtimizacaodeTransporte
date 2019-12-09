import numpy as np
import math, sys, csv, os, getopt
import simplex

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

def Monta_Obj(tab):
    obj = []
    for i in range(0, len(tab)):
        for j in range(0, len(tab[0])):
            obj.append(tab[i][j])
    return obj

def Rest_Linhas(tab):
    q_linhas = len(tab)
    q_colunas = len(tab[0])
    rl = []
    for i in range(0, q_linhas):
        rl.append(list(np.zeros(q_colunas*q_linhas)))
        for j in range(q_colunas*i, (q_colunas*i)+q_colunas):
            rl[i][j] = 1
    return rl

def Rest_Colunas(tab):
    q_linhas = len(tab)
    q_colunas = len(tab[0])
    rc = []
    for i in range(q_colunas):
        rc.append(list(np.zeros(q_colunas*q_linhas)))
        for j in range(i,q_linhas*q_colunas, q_colunas):
            rc[i][j] = 1
    return rc

def Retorna_Restricoes(tab):
    L = Rest_Linhas(tab)
    C = Rest_Colunas(tab)
    return ( L+C )

def Gera_Coeficientes(farmacias, solicitacoes):
    coef = []
    for i in farmacias:
        coef.append(i[3])
    for i in solicitacoes:
        coef.append(i[3])
    return coef

def Balancear_Modelagem(farmacias, solicitacoes):
    estoque = 0
    demanda = 0
    for e in farmacias:
        estoque += e[3]
    for s in solicitacoes:
        demanda += s[3]
    if(estoque > demanda):
        dif = estoque - demanda
        n = np.zeros(len(solicitacoes[0]))
        n[len(solicitacoes[0])-1] = dif
        ns = []
        for s in solicitacoes:
            ns.append(s)
        ns.append(n)
        solicitacoes = np.array(ns)
    elif(demanda > estoque):
        dif = demanda - estoque
        n = np.zeros(len(farmacias[0]))
        n[len(farmacias[0])-1] = dif
        n[0] = -1
        ns = []
        ns.append(n)
        for s in farmacias:
            ns.append(s)
        farmacias = np.array(ns)
    return farmacias, solicitacoes

## Leitura das coordenadas das lojas, estoque e solicitacoes
farmacias = np.loadtxt('t_farm.csv', delimiter=",", unpack=False, dtype='float')
solicitacoes = np.loadtxt('t_sol.csv', delimiter=",", unpack=False, dtype='float')

## Balanceamento da Modelagem
farmacias, solicitacoes = Balancear_Modelagem(farmacias, solicitacoes)
## Calculo dos Custos
tablecustos = CalculaDistancias(farmacias, solicitacoes)

# Montagem das restricoes
O = Monta_Obj(tablecustos)
R = Retorna_Restricoes(tablecustos)
C = Gera_Coeficientes(farmacias, solicitacoes)

custos = []
for i in range(len(tablecustos)):
    custos.append(list(np.zeros(len(tablecustos[0]))))
    for j in range(len(tablecustos[0])):
        custos[i][j] = tablecustos[i][j]

## Calculo da Solução
simplex.SimplexSolver().run_simplex(R, C, O, len(farmacias), len(solicitacoes), custos, 'min', ineq=[], enable_msg=True, latex=True)

