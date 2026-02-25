import os
import csv

def gerar_csv_padrao(time, jogador, diretorio_base):
    header_padrao = [['Rk,G,Date▲,Age,Tm,,Opp,,GS,MP,TS%,eFG%,ORB%,DRB%,TRB%,AST%,STL%,BLK%,TOV%,USG%,ORtg,DRtg,GmSc,BPM']]
    nome_arquivo = f"{jogador}.csv"
    # Verificar permissões
    os.chmod(diretorio_base, 0o777)  # Permissões completas para o diretório
    caminho_pasta = os.path.join(diretorio_base, time, 'Jogadores')
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
    caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
    with open(caminho_pasta, 'w', newline='\n', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerows(header_padrao)
        
        
# Caminho do diretório
dir_path = "C:\\Users\\SuperUser\\Documents\\Workspace\\Basquete Análise de Dados\\Times"
#os.chmod(dir_path, 0o777)  # Permissões completas para o diretório
# Verificar se o diretório existe
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

time = input()
nome_arquivo = input() + ".csv"

dir_path = os.path.join(dir_path, time, "Jogadores", nome_arquivo)

header_padrao = [['Rk,G,Date▲,Age,Tm,,Opp,,GS,MP,TS%,eFG%,ORB%,DRB%,TRB%,AST%,STL%,BLK%,TOV%,USG%,ORtg,DRtg,GmSc,BPM']]
        
# Agora você pode tentar acessar o diretório novamente
try:
    # Seu código para acessar o diretório
    with open(dir_path, 'w', newline='\n', encoding='utf-8') as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv)
        escritor_csv.writerows(header_padrao)
        
    print("Acesso bem-sucedido")
except PermissionError as e:
    print(f"Erro de permissão: {e}")