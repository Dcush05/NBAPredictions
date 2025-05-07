from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerDashboardByYearOverYear
from sklearn.linear_model import LinearRegression
import pandas as pd
import time

nba_player_stats = "data/all_nba_player_stats.csv"
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
                "Luka Doncic",
                "James Harden",
                "Damian Lillard", 
                "Jalen Brunson",
                "Jimmy Butler",
                "Trae Young",
                "Jayson Tatum",
                "Jaylen Brown",
                "Lamelo Ball",
                "Jamal Murray"                
                }



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

def forecast_player_2025(player_name, stat_columns=['W','L','PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'TOV']):
    df = pd.read_csv(nba_player_stats)

    player_df = df[df['PLAYER_NAME'] == player_name].copy()

    if player_df.empty:
        print(f"❌ No data found for {player_name}")
        return

    # Add numeric season for model training
    player_df['SEASON_NUMERIC'] = player_df['GROUP_VALUE'].str[:4].astype(int) + 1

    # Initialize list to hold forecast row
    future_season = 2025
    forecast_row = {
        'PLAYER_NAME': player_name,
        'GROUP_VALUE': '2024-25',
        'SEASON_NUMERIC': future_season
    }

    # Fit and forecast each stat
    for stat in stat_columns:
        x = player_df[['SEASON_NUMERIC']].values
        y = player_df[[stat]].values
        model = LinearRegression()
        model.fit(x, y)
        pred = model.predict([[future_season]])
        forecast_row[stat] = round(float(pred.item()), 2)

    forecast_df = pd.DataFrame([forecast_row])
    output_df = pd.concat([player_df, forecast_df], ignore_index=True)

    cols = output_df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('PLAYER_NAME')))
    output_df = output_df[cols]

    # Save to CSV
    filename = "data/" + player_name.lower().replace(" ", "_") + "_forecast.csv"
    output_df.to_csv(filename, index=False)
    print(f"✅ Forecast saved to {filename}")
 
def get_nba_players_stats():
    player_stats = pd.DataFrame()
    for names in player_names:
        df = fetch_player_season_stats(names, "Regular Season")
        player_stats = pd.concat([player_stats, df], ignore_index=True)
    cols = player_stats.columns.tolist()
    if 'PLAYER_NAME' in cols:
        cols.insert(0, cols.pop(cols.index('PLAYER_NAME')))
        player_stats = player_stats[cols]
    player_stats.to_csv(nba_player_stats, index=False)
    print("✅ Stats saved to " + nba_player_stats)



def main():
    get_nba_players_stats()
    for name in player_names:
        forecast_player_2025(name)
    
    

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

