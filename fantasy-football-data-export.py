import json
from espn_api.football import League
from datetime import datetime

def export_fantasy_data():
    league = League(league_id=1339878609, year=2024, espn_s2='AEBGoJjAS4SM7DHbWg6stHnFMDDYgdLKLg%2FebH3pNTwEbryMa%2FHlpJeGKcWxv9mf0nofghK7mLwIBHRDFN7f%2FDVizYWiW0aOtGX3noMSqDuTZVNXrdgmuP3cC4c%2FebOT66RxuM%2BbOsgJ4cbOSYXpMAwuYrOEbj%2FvWorQXyu1OB4tryxcfHdmZtF0v07%2B%2BNM84qJaRYDHjPgwcAAwUuRem3RaEpmEM3dk2N6cMsqaocPkG5pdZ5XnSmtWBVlznLCrb9IrgSITEiIJf9NzcWxxUg0E64PDCdkhiIHhf%2B6A%2BtWZeg%3D%3D', swid='{CAF63A66-37AB-46D6-B404-414B27C0A132}')
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
