import pandas as pd
from pulp import *


#Lista com nomes das fábricas
fabricas = ["3403208", "3423909", "3424402"]


#Capacidade de produção de cada fábrica
producao_fabrica = {"3403208":90000000, "3423909":56000000, "3424402": 90000000}


#Lista com nomes dos clientes
clientes = ["2301", "2302", "2303", "2304", "2305", "2306", "2307", "2308", "2309", "2310", "2311",
            "2312", "2313", "2314", "2315", "2316", "2317", "2318", "2319", "2320", "2321", "2322",
            "2323", "2324", "2325", "2326", "2327", "2328", "2329", "2330", "2331", "2332", "2333",
            "2334", "2335", "2336", "2337", "2338", "2339", "2340", "2341", "2342", "2343", "2344",
            "2345", "2346", "2347", "2348", "2349", "2350", "2351"]


#Demanda de cada cliente
demanda_clientes = {"2301":7886100, "2302":7041900, "2303":5899800, "2304":2661900, "2305":6418800,
                    "2306":3212700, "2307":6306300, "2308":4483500, "2309":7397400, "2310":4155900,
                    "2311":7222800, "2312":1337400, "2313":2138400, "2314":2625600, "2315":1210200,
                    "2316":1073400, "2317":1679700, "2318":1690800, "2319":2360400, "2320":5013300,
                    "2321":3526800, "2322":2470500, "2323":3472800, "2324":6741600, "2325":5167500,
                    "2326":5730900, "2327":7812900, "2328":6084300, "2329":6861600, "2330":6895800,
                    "2331":6066300, "2332":10731900, "2333":5295000, "2334":3759900, "2335":4685700,
                    "2336":1699200, "2337":3276600, "2338":2514300, "2339":3542700, "2340":3856500,
                    "2341":2626200, "2342":3322200, "2343":4034700, "2344":2686800, "2345":2376300,
                    "2346":3487800, "2347":4851900, "2348":3892200, "2349":5231100, "2350":4359300,
                    "2351":5274300 }


# Lista do custo de para cada rota de transporte
custos = [ #Clientes
#2301  2302  2303  2304  2305  2306  2307  2308  2309  2310  2311  2312  2313  2314  2315  2316  2317  2318  2319  2320  2321  2322  2323  2324  2325  2326  2327  2328  2329  2330  2331  2332  2333  2334  2335  2336  2337  2338  2339  2340  2341  2342  2343  2344  2345  2346  2347  2348  2349  2350  2351
[0.56, 0.51, 0.43, 0.47, 0.50, 0.55, 0.53, 0.55, 0.43, 0.71, 0.37, 0.79, 0.77, 0.71, 0.84, 0.84, 0.84, 0.84, 0.70, 0.73, 0.77, 0.69, 0.75, 0.71, 0.63, 0.70, 0.72, 0.72, 0.76, 0.76, 0.70, 0.69, 0.67, 0.69, 0.69, 0.00, 0.00, 0.00, 0.87, 0.97, 0.92, 0.91, 0.99, 0.63, 0.64, 0.64, 0.28, 0.28, 0.30, 0.36, 0.41],  #3403208 Fabricas
[0.00, 0.00, 0.00, 0.00, 0.26, 0.00, 0.00, 0.26, 0.27, 0.29, 0.26, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.28, 0.25, 0.29, 0.28, 0.31, 0.32, 0.43, 0.29, 0.34, 0.60, 0.27, 0.27, 0.48, 0.46, 0.46, 0.55, 0.61, 0.58, 0.57, 0.61, 0.00, 0.00, 0.00, 0.68, 0.72, 0.61, 0.68, 0.63],  #3423909
[0.42, 0.38, 0.37, 0.40, 0.40, 0.37, 0.43, 0.37, 0.48, 0.28, 0.56, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.29, 0.28, 0.28, 0.29, 0.25, 0.29, 0.27, 0.28, 0.21, 0.31, 0.27, 0.29, 0.28, 0.27, 0.27, 0.29, 0.29, 0.72, 0.70, 0.70, 0.00, 0.00, 0.00, 0.00, 0.00, 0.48, 0.49, 0.47, 0.90, 0.96, 1.05, 1.02, 1.09],  #3424402
]


#Transformação da lista de custos em um dicionário
custos = makeDict([fabricas, clientes], custos, 0)


#Criação da variável 'problema', a qual conterá os sistemas de equações da LP
problema = LpProblem("Problema de Distribuicao Fabrica-Cliente", LpMinimize)


#Criação de tuplas com todas as rotas possíveis entre fabrica e clientes
rotas = [(f, c) for f in fabricas for c in clientes]


#Dicionaário criado para armazenar todas as variáveis envolvidas nesse problema
variaveis = LpVariable.dicts("Rota", (fabricas, clientes), 0, None, LpInteger)


#Função objetivo que deve ser maximizada
problema += (
    lpSum([variaveis[f][c] * custos [f][c] for (f, c) in rotas]),
    f"Soma dos custos de transporte",
)


#Restrições de distribuição máximas para cada fábrica
for f in fabricas:
    problema += (
        lpSum([variaveis[f][c] for c in clientes]) <= producao_fabrica[f],
        f"Total_produtos_que_saem_da_fabrica_{f}",
    )


#Restrições de demanda mínima para cada cliente
for c in clientes:
    problema += (
        lpSum([variaveis[f][c] for f in fabricas]) >= demanda_clientes[c],
        f"Total_produtos_com_cliente_{c}",
    )


#Resolução do modelo referente ao problema
problema.solve()


#Imprime o status da solução do problema
print("Status:", LpStatus[problema.status])


#Criação da lista de tuplas com as variaveis para manipulação de strings para gravar os resultados em .XSLX
lista_vars = []


#Imprime o custo de transporte de cada fábrica para cada cliente
for v in problema.variables():
    print(v.name, "=", v.varValue)
    lista_vars.append((f"{v.name[5:12]}", f"{v.name[13:]}", f"{v.varValue}"))


#Nome do arquivo de saída. Do jeito que está, será salvo de onde está rodando esse arquivo .py
file_name = 'saida.xlsx'

#Criando df Pandas
df = pd.DataFrame(lista_vars, columns =["Fabrica", "Cliente", "Custo Rota"])

#Gravando os resultados no .xlsx
df.to_excel(file_name, index=False)

#Imprime o custo total do transporte entre fábricas e clientes
print("Total de custo com transporte: ", value(problema.objective))
