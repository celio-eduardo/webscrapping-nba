import os
import pandas as pd
from datetime import datetime

# Mapeamento de meses em inglês para números
meses = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}

# Função para converter data
def converter_data(data_str):
    partes = data_str.split()
    mes = meses[partes[0]]
    dia = partes[1].rstrip(',')
    ano = partes[2]
    return f"{dia}_{mes}_{ano}"

# Função para processar o cabeçalho
def processar_cabecalho(cabecalho):
    times, data_str = cabecalho.split(' Box Score, ')
    time_visitante, time_casa = times.split(' at ')
    data_formatada = converter_data(data_str)
    return time_casa, time_visitante, data_formatada

# Função para salvar dados
def salvar_dados(time, adversario, data_formatada, dados, tipo_jogo, diretorio_base):
    nome_arquivo = f"{data_formatada} - {adversario}.csv"
    caminho_pasta = os.path.join(diretorio_base, time, tipo_jogo)
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
    dados.to_csv(caminho_arquivo, index=False)
    print(f"Dados salvos em: {caminho_arquivo}")

# Função principal
def processar_arquivos_xls(nome_cabecalho, caminho_arquivos, diretorio_base):
    
    time_casa, time_visitante, data_formatada = processar_cabecalho(nome_cabecalho)

    
      # Definir os arquivos
    arquivos = [
        os.path.join(caminho_arquivos, "sportsref_download.csv"),
        os.path.join(caminho_arquivos, "sportsref_download (1).csv"),
        os.path.join(caminho_arquivos, "sportsref_download (2).csv"),
        os.path.join(caminho_arquivos, "sportsref_download (3).csv")
    ]

    # Ler os arquivos .csv
    dados_partida_casa = pd.read_csv(arquivos[0])
    dados_partida_visitante = pd.read_csv(arquivos[1])
    dados_primeiro_quarto_casa = pd.read_csv(arquivos[2])
    dados_primeiro_quarto_visitante = pd.read_csv(arquivos[3])

    # Salvar dados do time da casa
    salvar_dados(time_casa, time_visitante, data_formatada, dados_partida_casa, 'Jogos Totais', diretorio_base)
    salvar_dados(time_casa, time_visitante, data_formatada, dados_primeiro_quarto_casa, 'Primeiro Quarto', diretorio_base)

    # Salvar dados do time visitante
    salvar_dados(time_visitante, time_casa, data_formatada, dados_partida_visitante, 'Jogos Totais', diretorio_base)
    salvar_dados(time_visitante, time_casa, data_formatada, dados_primeiro_quarto_visitante, 'Primeiro Quarto', diretorio_base)

if __name__ == '__main__':
    nome_cabecalho = input('Digite o cabeçalho da partida: ')
    caminho_arquivos = 'C:\\Users\\SuperUser\\Documents\\Workspace\\Basquete Análise de Dados\\Dados Provisorios Tratar'
    diretorio_base = 'C:\\Users\\SuperUser\\Documents\\Workspace\\Basquete Análise de Dados\\Times'
    processar_arquivos_xls(nome_cabecalho, caminho_arquivos, diretorio_base)