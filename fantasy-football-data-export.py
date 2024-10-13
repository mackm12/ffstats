import json
import os
import logging
from datetime import datetime
from espn_api.football import League

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def export_fantasy_data():
    logging.info("Starting fantasy football data export")

    try:
        # Initialize the League object with environment variables
        league = League(
            league_id=int(os.environ['LEAGUE_ID']),
            year=2024,
            espn_s2=os.environ['ESPN_S2'],
            swid=os.environ['SWID']
        )
        logging.info(f"Successfully connected to league: {league.league_id}")

        # Fetch box scores (adjust the week number as needed)
        box_scores = league.box_scores(12)
        logging.info(f"Retrieved box scores for week 12")

        data = []
        for i, matchup in enumerate(box_scores, 1):
            # Home team data
            for player in matchup.home_lineup:
                data.append({
                    'Game': i,
                    'Team': matchup.home_team.team_name,
                    'Is_Home': True,
                    'Team_Score': matchup.home_score,
                    'Player_Name': player.name,
                    'Player_Position': player.position,
                    'Player_Points': player.points
                })
            
            # Away team data
            for player in matchup.away_lineup:
                data.append({
                    'Game': i,
                    'Team': matchup.away_team.team_name,
                    'Is_Home': False,
                    'Team_Score': matchup.away_score,
                    'Player_Name': player.name,
                    'Player_Position': player.position,
                    'Player_Points': player.points
                })

        # Prepare the output with a timestamp
        output = {
            'last_updated': datetime.now().isoformat(),
            'data': data
        }

        # Write data to JSON file
        with open('fantasy_football_data.json', 'w') as file:
            json.dump(output, file, indent=2)
        
        logging.info("Data successfully exported to fantasy_football_data.json")

    except KeyError as e:
        logging.error(f"Environment variable not set: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    export_fantasy_data()
