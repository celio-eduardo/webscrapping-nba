import os

# Lista dos nomes dos times
times = [
    "Atlanta Hawks",
    "Boston Celtics",
    "Brooklyn Nets",
    "Chicago Bulls",
    "Charlotte Hornerts",
    "Cleveland Cavaliers",
    "Dallas Maverics",
    "Denver Nuggets",
    "Detroit Pistons",
    "Golden State Warriors",
    "Houston Rockets",
    "Indiana Pacers",
    "Los Angeles Clippers",
    "Los Angeles Lakers",
    "Memphis Grizzlies",
    "Miami Heat",
    "Milwaukee Bucks",
    "Minnesota Timberwolvs",
    "New Orleans Pelicans",
    "New York Knicks",
    "Oklahoma City Thunders",
    "Orlando Magic",
    "Philadelphia 76ers",
    "Phoenix Suns",
    "Portland Trail Blazers",
    "Sacramento Kings",
    "San Antonio Spurs",
    "Toronto Raptors",
    "Utah Jazz",
    "Washington Wizards"
]

# Diretório base onde as pastas serão criadas
diretorio_base = 'C:\\Users\\SuperUser\\Documents\\Workspace\\Basquete Análise de Dados\\Times'

def criar_pastas(times, diretorio_base):
    for time in times:
        caminho_time = os.path.join(diretorio_base, time)
        caminho_jogos_totais = os.path.join(caminho_time, 'Jogos Totais')
        caminho_primeiro_quarto = os.path.join(caminho_time, 'Primeiro Quarto')
        caminho_jogadores = os.path.join(caminho_time, 'Jogadores')
        
        try:
            os.makedirs(caminho_jogos_totais, exist_ok=True)
            os.makedirs(caminho_primeiro_quarto, exist_ok=True)
            print(f'Pastas criadas: {caminho_jogos_totais} , {caminho_primeiro_quarto} e {caminho_jogadores}')
        except OSError as e:
            print(f'Erro ao criar as pastas {caminho_time}: {e}')

if __name__ == '__main__':
    criar_pastas(times, diretorio_base)