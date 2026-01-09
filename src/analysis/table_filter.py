from utils.logger import get_logger

logger = get_logger()

class TableFilter: 

    def __init__(self, data):
        logger.debug("Loading TableFilter")
        self.data = data
        self.standings = data['standings'][0]['table']
        logger.info("Loaded EPL table standings")

    def get_full_table(self):
        logger.debug("Retrieving entire table")
        return self.standings
    
    def get_team_by_name(self, team_name):
        logger.debug(f"Searching for team: {team_name}")

        for team in self.standings:
            if team_name.lower() in team['team']['name'].lower():
                logger.info(f"Found team: {team['team']['name']}")
                return team
            
        logger.warning(f"Team not found: {team_name}")
        return None
    
    def calculate_form(self, team_id, matches_data):
        team_matches = []

        for match in matches_data.get('matches', []):
            if match['status'] != 'FINISHED':
                continue
            
            home_team_id = match['homeTeam']['id']
            away_team_id = match['awayTeam']['id']
        
            if home_team_id == team_id or away_team_id == team_id:
                team_matches.append(match)
    
        # sortera efter datum, senast först
        team_matches.sort(key=lambda x: x['utcDate'], reverse=True)
    
        # Ta 5 senaste
        recent_matches = team_matches[:5]
    
        form = ""

        for match in reversed(recent_matches):  # Äldst först
            home_score = match['score']['fullTime']['home']
            away_score = match['score']['fullTime']['away']
        
            if match['homeTeam']['id'] == team_id:
                if home_score > away_score:
                    form += "W"
                elif home_score < away_score:
                    form += "L"
                else:
                    form += "D"
            else:
                if away_score > home_score:
                    form += "W"
                elif away_score < home_score:
                    form += "L"
                else:
                    form += "D"

        return form if form else "N/A"