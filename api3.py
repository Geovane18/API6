import pandas as pd
import numpy as np
import matplotlib as plt

#define o caminho do arquivo no computador
File = 'C:/Users/Pichau/Downloads/'

#abre os arquivos necessários
df = pd.read_csv(File+'Rotas.csv', sep=',', decimal ='.')
df2 = pd.read_csv(File+'Clientes.csv', sep=',', decimal ='.')
df3  = pd.read_csv(File+'Fabricas.csv', sep=',', decimal ='.', encoding='latin1')

#checagem dos arquivos
##1
df.info()
##2
df2.info()
##3
df3.info()

#integra o df de Rotas com o df de Clientes e Fabricas
rotas_final = df.merge(df2, left_on='CO.Cliente',
	                    right_on='CO.Cliente',
	                    how='inner').merge(df3, left_on='CO.Fabrica',
	                                       right_on='CO.Fabrica',
	                                       how='inner')

#checagem do df final
rotas_final.info()

#visualiza o df final
rotas_final.head(5)

#cria nova coluna com condição
rotas_final['Capacidade'] = None
rotas_final.loc[rotas_final['Veiculo'] == 'P24', 'Capacidade'] = 3600
rotas_final.loc[rotas_final['Veiculo'] == 'P12', 'Capacidade'] = 1800

#cria nova coluna com cálculo
rotas_final['Produtividade'] = rotas_final['Qtd.Transp'] / rotas_final['Capacidade'] * 100

#Análises
##Filtros

fabricas = rotas_final['CO.Fabrica'].unique()
print(fabricas)

#análise segmentada de uma fábrica

co_fabrica = 3423909
incoterm = 'CIF'

df_filtrado = rotas_final[(rotas_final['CO.Fabrica'] == co_fabrica) &
                           (rotas_final['Incoterm'] == incoterm)]
clientes = df_filtrado['CO.Cliente'].unique()
print(clientes)

#exportar a lista de clientes
with open('clientes.txt','w') as file:
     for client in clientes:
         file.write(str(client) + '\n')


#Frete médio por fabrica e cliente


df_filtrado['frete/unidade'] = df_filtrado['Vlr.Frete'] / df_filtrado['Qtd.Transp']
frete_media = df_filtrado.groupby(['CO.Fabrica',                   'CO.Cliente'])['frete/unidade'].mean().reset_index()
frete_media.info()
print(frete_media)

frete_media.to_csv('Frete.csv', index=False)



#exporta o novo df para csv
rotas_final.to_csv('Rotas_final.csv', index=False)

