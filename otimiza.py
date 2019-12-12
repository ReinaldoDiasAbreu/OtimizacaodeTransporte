import numpy as np
import math, sys, csv, os, getopt, os.path

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
            if sol[j][0] == 0 or farm[i][0] == -1:
                custos[i][j] = 0
            else:
                custos[i][j] = round(Haversine(farm[i][1],farm[i][2], sol[j][1],sol[j][2]))
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
    for j in solicitacoes:
        coef.append(j[3])
    return coef

def Balancear_Modelagem(farmacias, solicitacoes):
    estoque = 0
    demanda = 0
    for e in farmacias:
        estoque += e[3]
    for s in solicitacoes:
        demanda += s[3]
    if(estoque > demanda):
        b_est = -1
        dif = estoque - demanda
        n = np.zeros(len(solicitacoes[0]))
        n[len(solicitacoes[0])-1] = dif
        ns = []
        for s in solicitacoes:
            ns.append(s)
        ns.append(n)
        solicitacoes = np.array(ns)
    elif(demanda > estoque):
        b_est = 1
        dif = demanda - estoque
        n = np.zeros(len(farmacias[0]))
        n[len(farmacias[0])-1] = dif
        n[0] = -1
        ns = []
        for s in farmacias:
            ns.append(s)
        ns.append(n)
        farmacias = np.array(ns)
    else:
        b_est = 0
    return farmacias, solicitacoes, b_est

# Leitura dos parametros
param = sys.argv[1:]

if(len(param) == 2): #Verificando se dois parametros foram passados
    # Testando a existencia dos arquivos
    f1 = os.path.exists(param[0])
    f2 = os.path.exists(param[1])

    if(f1 == True and f2 == True):
        # Iniciando o algoritmo
        print("ALGORITMO DE OTIMIZAÇÃO DE TRANSPORTE")
        print(" - Iniciando processamento dos dados:")
        print("     Fornecimento: ", param[0])
        print("     Solicitações: ", param[1])

        ## Leitura das coordenadas das lojas, estoque e solicitacoes
        farmacias = np.loadtxt(param[0], delimiter=",", unpack=False, dtype='float')
        solicitacoes = np.loadtxt(param[1], delimiter=",", unpack=False, dtype='float')

        ## Balanceamento da Modelagem
        farmacias, solicitacoes, b_est = Balancear_Modelagem(farmacias, solicitacoes)

        ## Calculo dos Custos
        tablecustos = CalculaDistancias(farmacias, solicitacoes)
        #print(tablecustos)
        # Montagem das restricoes
        O = Monta_Obj(tablecustos)
        R = Retorna_Restricoes(tablecustos)
        C = Gera_Coeficientes(farmacias, solicitacoes)
        O = np.array(O)
        
        custos = []
        for i in range(len(tablecustos)):
            custos.append(list(np.zeros(len(tablecustos[0]))))
            for j in range(len(tablecustos[0])):
                custos[i][j] = tablecustos[i][j]

        # Gera string com a modelagem
        c = 0
        string = ""
        for i in range(len(tablecustos)):
            for j in range(len(tablecustos[0])):
                string += str(int(tablecustos[i][j])) + "|"
            string += str(int(farmacias[c][3])) + "|"
            string += "\n"
            c+=1
        
        for i in solicitacoes:
            string += str(int(i[3])) + "|"

        print("Farmácias: ", len(farmacias))
        print("Clientes: ", len(solicitacoes))

        if(b_est == -1):
            print("Estoque maior que demanda! Cliente ", len(solicitacoes), " foi adicionado!")
        elif(b_est == 1):
            print("Estoque menor que demanda! Loja ", len(farmacias), " foi adicionada!")

        if(len(farmacias) <= 18): # Máximo suportado
            with open("modelagem.txt", "w") as tex:
                tex.write(string)
            print("Arquivo: modelagem.txt gerado...")
        else:
            print("Máximo de 18 lojas é suportado!!!")

    else:
        print("ERRO: Arquivos de entrada não foram identificados.")
else:
    print("python3 otimiza.py <csv_fornecimento> <csv_destinos>")
