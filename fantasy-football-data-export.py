import json
from espn_api.football import League
from datetime import datetime

def export_fantasy_data():
    league = League(
        league_id=int(os.environ['LEAGUE_ID']),
        year=2024,
        espn_s2=os.environ['ESPN_S2'],
        swid=os.environ['SWID'] 
    box_scores = league.box_scores(12)

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

    # Add a timestamp to the data
    output = {
        'last_updated': datetime.now().isoformat(),
        'data': data
    }

    with open('fantasy_football_data.json', 'w') as file:
        json.dump(output, file, indent=2)

    print("Data exported to fantasy_football_data.json")

if __name__ == "__main__":
    export_fantasy_data()
