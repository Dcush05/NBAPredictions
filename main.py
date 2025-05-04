from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerDashboardByYearOverYear
import pandas as pd
import time



def get_player_id(name):
    player_dict = players.find_players_by_full_name(name)
    return player_dict[0]['id'] if player_dict else None

def fetch_player_season_stats(player_name, season_type):
    player_id = get_player_id(player_name)
    if player_id is None:
        print(f"Player {player_name} not found.")
        return

    print(f"Fetching data for {player_name} (ID: {player_id})...")

    stats = PlayerDashboardByYearOverYear(
        player_id=player_id,
        season_type_playoffs=season_type,
        per_mode_detailed='PerGame'
    )

    time.sleep(1)  # safety

    df = stats.get_data_frames()[1]

    df['PLAYER_NAME'] = player_name
    df = df[df['GROUP_VALUE'].isin([
        '2019-20', '2020-21', '2021-22', '2022-23', '2023-24'
    ])]

    return df
player_names = {"Lebron James",
                "Stephen Curry",
                "Kevin Durant",
                "Kawhi Leonard",
                "Nikola Jokic",
                "Giannis Antetokounmpo",
                "Anthony Davis",
                "Draymond Green",
                "Klay Thompson",
                "Chris Paul",
                "Kyle Lowry",
                "Russell Westbrook",
                "Kyrie Irving",
                }


 
def get_nba_players_stats():
    player_stats = pd.DataFrame()
    for names in player_names:
        df = fetch_player_season_stats(names, "Regular Season")
        player_stats = pd.concat([player_stats, df], ignore_index=True)
    cols = player_stats.columns.tolist()
    if 'PLAYER_NAME' in cols:
        cols.insert(0, cols.pop(cols.index('PLAYER_NAME')))
        player_stats = player_stats[cols]
    player_stats.to_csv("data/nba_player_stats.csv", index=False)
    print("✅ Stats saved to nba_player_stats.csv")



def main():
    get_nba_players_stats()
    
    

if __name__ == '__main__':
    main()


    
'''Hall of Famers
Lebron James
Stephen Curry
Kevin Durant
Kawhi Leonard
Nikola Jokic
Giannis Antetokounmpo
Anthony Davis
Draymond green
Klay Thompson
Chris Paul
Kyle Lowry
Russel Westbrook
Kyrie Irving'''

