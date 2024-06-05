import sidrapy
import pandas as pd
import os


# cria função para acessar os dados de população residente 
# ano 2010 Tabela SIDRA 3145
# ano 2022 Tabela SIDRA 9514

def func_pop(tab):
    pop_pb = sidrapy.get_table(table_code = tab,
    territorial_level = "6",
    ibge_territorial_code = "all",
    period = "all")
    pop_mun_pb = (
    pop_pb
    .loc[1:, ['D1C','D1N','V']]
    .rename(columns = {
        'V':'pop_res','D1C':'cod_municipio','D1N':'municipio'})
    .assign(uf = lambda x : [x[0:2] for x in  x['cod_municipio']],
            municipio = lambda x : x['municipio'].str.replace('- PB',''),
            pop_res = lambda x : x['pop_res'].astype(float),
            cod_municipio = lambda x : x['cod_municipio'].astype(int))
    .pipe(lambda x : x.loc[x.uf == '25']) 
)
    return pop_mun_pb 

# # função para pegar os dados de 2010 e 2021
# # Tratamento dos dados mara montar df 2010 e 2021

 função para importar os dados do PIB para os anos de 2010 e 2021
def fuc_pib(ano):
    df_pib_mun_pb = pd.read_csv('tabelas/vab_pib_paraiba.csv', sep=',')
    pib_mun_pb_ano = (
    df_pib_mun_pb
    .loc[0:,['Ano',
             'cod_municipio',
             'nome_municipio',
             'cod_mesorregiao',
             'nome_mesoregiao',
             'cod_microrregiao',
             'nome_microrregiao',
             'pib_precos_corrente',
             'pib_per_capita_pc']]
    .assign(pib_precos_corrente = lambda x : x['pib_precos_corrente'].astype(float),
            pib_per_capita_pc = lambda x : x['pib_per_capita_pc'].str.replace(',','.').astype(float),
            cod_municipio = lambda x : x['cod_municipio'].astype(int))
    .pipe(lambda x : x.loc[x.Ano == ano])
)
    return pib_mun_pb_ano