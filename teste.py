import os
import pandas as pd
import csv

def salvar_dados(dados):
    nome_arquivo = f"input.csv"
    #print(dados)
    caminho_pasta = os.path.abspath('C:\\Users\\SuperUser\\Documents\\Workspace\\Basquete Análise de Dados')
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
    with open(caminho_arquivo, 'w', newline='\n', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerows(dados)
    
def limpar_dados(dados):
    # Dividir os dados em linhas
    linhas = dados.split('\n')
    # Ignorar as três primeiras linhas
    linhas = linhas[4:]
    # Dividir cada linha em colunas
    dados_processados = [linha.split(',') for linha in linhas if linha]
    return dados_processados

with open('input.txt', 'r') as file:
    input_data = file.read()
    input_data = limpar_dados(input_data)
    saida = salvar_dados(input_data)
