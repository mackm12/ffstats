import requests
import json
from datetime import datetime

def fetch_iowa_womens_basketball_schedule(season):
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/womens-college-basketball/teams/2294/schedule"
    params = {
        "season": season
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    return response.json()

def parse_schedule(data):
    schedule = []
    for event in data.get('events', []):
        try:
            # Identify Iowa and opponent
            iowa_team = next(team for team in event['competitions'][0]['competitors'] if team['team']['id'] == '2294')
            opponent_team = next(team for team in event['competitions'][0]['competitors'] if team['team']['id'] != '2294')

            game = {
                'date': datetime.strptime(event['date'], "%Y-%m-%dT%H:%MZ").strftime("%Y-%m-%d"),
                'time': datetime.strptime(event['date'], "%Y-%m-%dT%H:%MZ").strftime("%H:%M"),
                'opponent': opponent_team['team']['displayName'],
                'home_away': iowa_team['homeAway'].capitalize() if iowa_team['homeAway'] != 'neutral' else 'Neutral',
                'venue': event['competitions'][0]['venue']['fullName'] if 'venue' in event['competitions'][0] else 'TBA',
                'tv_network': 'N/A'
            }

            # Safely get TV network information
            broadcasts = event['competitions'][0].get('broadcasts', [])
            if broadcasts:
                networks = broadcasts[0].get('names', [])
                game['tv_network'] = networks[0] if networks else 'N/A'

            schedule.append(game)
        except KeyError as e:
            print(f"Warning: Could not parse game data. KeyError: {e}")
            print(f"Problematic event data: {json.dumps(event, indent=2)}")
        except StopIteration:
            print(f"Warning: Could not identify Iowa or opponent team.")
            print(f"Problematic event data: {json.dumps(event, indent=2)}")

    return schedule

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    season = 2025  # Change this to the desired season
    filename = f"iowa_womens_basketball_schedule_{season}.json"

    try:
        raw_data = fetch_iowa_womens_basketball_schedule(season)
        schedule = parse_schedule(raw_data)
        save_to_json(schedule, filename)
        print(f"Schedule for {season} season has been saved to {filename}")
        print(f"Total games parsed: {len(schedule)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()