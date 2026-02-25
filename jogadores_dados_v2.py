import os
import pandas as pd
import csv

def gerar_csv_padrao(time, jogador, diretorio_base):
    header_padrao = [['Rk,G,Date,Age,Tm,,Opp,,GS,MP,FG,FGA,FG%,3P,3PA,3P%,FT,FTA,FT%,ORB,DRB,TRB,AST,STL,BLK,TOV,PF,PTS,GmSc,+/-']]
    nome_arquivo = f"{jogador}_GAME_LOG.csv"
    caminho_pasta = os.path.join(diretorio_base, time, 'Jogadores')
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
    with open(caminho_arquivo, 'w', newline='\n', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerows(header_padrao)
        
        
def salvar_dados(time, jogador, dados, diretorio_base):
    nome_arquivo = f"{jogador}_GAME_LOG.csv"
    # Verificar permissões
    os.chmod(diretorio_base, 0o777)  # Permissões completas para o diretório
    caminho_pasta = os.path.join(diretorio_base, time, 'Jogadores')
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
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

# Função principal
def processar_arquivos_xls(nome_jogador, time_base, dados, diretorio_base):
    # Limpar o arquivo de dados
    dados_jogador = limpar_dados(dados)

    # Salvar dados do time da casa
    salvar_dados(time_base, nome_jogador, dados_jogador, diretorio_base)
