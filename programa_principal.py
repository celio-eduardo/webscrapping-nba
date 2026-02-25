import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Passo 1: Carregar Dados
def carregar_dados(pasta):
    arquivos = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith('.csv')]
    dados = pd.concat([pd.read_csv(arquivo) for arquivo in arquivos])
    return dados

# Passo 2: Pré-processamento de Dados
def preprocessar_dados(dados):
    # Filtrar jogadores que jogaram
    dados = dados[dados['MP'] != '-9999']
    dados = dados.dropna()  # Exemplo de limpeza de dados
    return dados

# Passo 3: Cálculo de Estatísticas
def calcular_estatisticas(dados, coluna):
    media = dados[coluna].mean()
    mediana = dados[coluna].median()
    moda = dados[coluna].mode()[0] if not dados[coluna].mode().empty else 'N/A'
    variancia = dados[coluna].var()
    desvio_padrao = dados[coluna].std()

    estatisticas = {
        'Média': media,
        'Mediana': mediana,
        'Moda': moda,
        'Variância': variancia,
        'Desvio Padrão': desvio_padrao
    }
    return estatisticas

# Passo 4: Visualização de Dados
def visualizar_dados(dados, coluna, titulo, jogador):
    plt.figure(figsize=(10, 6))
    sns.histplot(dados[coluna], bins=20, kde=True)
    plt.title(f'Distribuição de {titulo} - {jogador}')
    plt.xlabel(titulo)
    plt.ylabel('Frequência')
    plt.savefig(f'resultados/{jogador}_{titulo}.png')
    plt.close()

# Passo 5: Salvar Resultados
def salvar_resultados(jogador, estatisticas, intervalo):
    with open(f'resultados/{jogador}_estatisticas_{intervalo}.txt', 'w') as f:
        f.write(f'Estatísticas para {jogador} - Últimas {intervalo} partidas\n')
        for chave, valor in estatisticas.items():
            f.write(f'{chave}: {valor}\n')

# Passo 6: Automatização
def automatizar_processo(pasta_partidas, pasta_primeiro_quarto):
    dados_partidas = carregar_dados(pasta_partidas)
    dados_primeiro_quarto = carregar_dados(pasta_primeiro_quarto)
    
    dados_partidas = preprocessar_dados(dados_partidas)
    dados_primeiro_quarto = preprocessar_dados(dados_primeiro_quarto)

    jogadores = dados_partidas['Starters'].unique()
    intervalos = [20, 15, 10, 5]

    if not os.path.exists('resultados'):
        os.makedirs('resultados')

    for jogador in jogadores:
        dados_jogador_partidas = dados_partidas[dados_partidas['Starters'] == jogador]
        dados_jogador_primeiro_quarto = dados_primeiro_quarto[dados_primeiro_quarto['Starters'] == jogador]

        for intervalo in intervalos:
            if len(dados_jogador_partidas) >= intervalo:
                dados_intervalo_partidas = dados_jogador_partidas.tail(intervalo)
                dados_intervalo_primeiro_quarto = dados_jogador_primeiro_quarto.tail(intervalo)

                estatisticas_partida = calcular_estatisticas(dados_intervalo_partidas, 'PTS')
                estatisticas_primeiro_quarto = calcular_estatisticas(dados_intervalo_primeiro_quarto, 'FG')

                visualizar_dados(dados_intervalo_partidas, 'PTS', f'Total de Pontos na Partida - Últimas {intervalo} Partidas', jogador)
                visualizar_dados(dados_intervalo_primeiro_quarto, 'FG', f'Cestas no Primeiro Quarto - Últimas {intervalo} Partidas', jogador)

                salvar_resultados(jogador, estatisticas_partida, intervalo)
                salvar_resultados(jogador, estatisticas_primeiro_quarto, intervalo)

if __name__ == '__main__':
    pasta_partidas = 'caminho/para/pasta/partidas'
    pasta_primeiro_quarto = 'caminho/para/pasta/primeiro_quarto'
    automatizar_processo(pasta_partidas, pasta_primeiro_quarto)