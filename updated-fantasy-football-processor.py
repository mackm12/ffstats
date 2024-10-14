import json
import requests
from collections import defaultdict

def fetch_latest_data():
    # Replace with the actual URL of your data source
    url = "https://your-data-source-url.com/fantasy_football_data.json"
    response = requests.get(url)
    return response.json()

def process_fantasy_data(data):
    games = defaultdict(lambda: defaultdict(lambda: {'players': [], 'total_score': 0}))
    
    for entry in data:
        game_num = entry['Game']
        team_name = entry['Team']
        is_home = entry['Is_Home']
        team_score = entry['Team_Score']
        player_name = entry['Player_Name']
        player_position = entry['Player_Position']
        player_points = entry['Player_Points']
        
        team_key = 'home' if is_home else 'away'
        
        games[game_num][team_key]['team_name'] = team_name
        games[game_num][team_key]['total_score'] = team_score
        games[game_num][team_key]['players'].append({
            'name': player_name,
            'position': player_position,
            'points': player_points
        })
    
    return games

def main():
    json_data = fetch_latest_data()
    
    processed_data = process_fantasy_data(json_data['data'])
    
    # Save the processed data to a new JSON file
    with open('processed_fantasy_football_data.json', 'w') as outfile:
        json.dump(processed_data, outfile, indent=2)
    
    print("Processed data has been saved to 'processed_fantasy_football_data.json'")

if __name__ == "__main__":
    main()
