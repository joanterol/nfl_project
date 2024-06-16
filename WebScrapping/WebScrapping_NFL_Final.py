import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

# Creamos la lista de temporadas
seasons = [str(season) for season in range(2003, 2024)]
print(f' number of seasons: {len(seasons)}')

# Creamos la lista con los nombres de los equipos abreviados
team_abbrs = ['crd', 'atl',  'rav', 'buf', 'car', 'chi', 'cin', 'cle', 'dal', 'den', 'det', 'gnb', 'htx', 'clt', 
              'jax', 'kan', 'sdg', 'ram', 'rai', 'mia', 'min', 'nwe', 'nor', 'nyg', 'nyj', 'phi', 'pit', 'sea', 
              'sfo', 'tam', 'oti', 'was']
print(f' number of teams: {len(team_abbrs)}')

# Creamos un df vacío donde añadiremos los datos    
nfl_df = pd.DataFrame()


# Creamos un loop que recorra las temporadas y los equipos
for season in seasons:
    for team in team_abbrs: 
        print(f'Getting data for {team} in {season}')
        # Obtenemos la url de la página web
        url = f'https://www.pro-football-reference.com/teams/{team}/{season}/gamelog/'
        print(url)

        # Realizamos la solicitud al sitio web
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscamos la tabla de estadísticas ofensivas
        off_table = soup.find('table', {'id': 'gamelog' + season})
        off_df = pd.read_html(str(off_table), header=1)[0]

        # Buscamos la otra tabla específica (modifica según la lógica de tu página web)
        play_off_table = soup.find('table', {'id': 'playoff_gamelog' + season})
        
        # Verificar si la tabla existe antes de procesarla
        if play_off_table:
            play_off_df = pd.read_html(str(play_off_table), header=1)[0]
            
            # Concatenar con el DataFrame existente
            team_df = pd.concat([off_df, play_off_df], ignore_index=True)
        else:
            team_df = off_df

        # Insertamos la temporada y el equipo
        team_df.insert(loc=0, column='Season', value=season)
        team_df.insert(loc=2, column='Team', value=team.upper())
        print(team_df)

        # Concatenamos los team gamelog a nfl_df
        nfl_df = pd.concat([nfl_df, team_df], ignore_index=True)

        print(nfl_df)

        time.sleep(random.randint(4, 5))
    nfl_df.to_csv(f'C:/Users/terol/OneDrive/Escritorio/TFG/WebScrapping/data/nfl_df{season}.csv', index=False)
    
print(nfl_df)

# nfl_df.to_csv('C:/Users/terol/OneDrive/Escritorio/TFG/WebScrapping/data/nfl_df.csv', index=False)