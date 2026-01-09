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
    
    def get_top_n(self, n=4):
        if n < 1 or n > len(self.standings):
            logger.warning(f"Invalid number of teams(n={n}), returning full table")
            return self.standings
        logger.info(f"Retrieving top {n} teams")
        return self.standings[:n]
    
    def get_bottom_n(self, n=3):
        if n < 1 or n > len(self.standings):
            logger.warning(f"Invalid number of teams(n={n}), returning full table")
            return self.standings
        
        logger.info(f"Retrieving bottom {n} teams")
        return self.standings[-n:]
    
    def get_team_by_name(self, team_name):
        logger.debug(f"Searching for team: {team_name}")

        for team in self.standings:
            if team_name.lower() in team['team']['name'].lower():
                logger.info(f"Found team: {team['team']['name']}")
                return team
            
        logger.warning(f"Team not found: {team_name}")
        return None
    
    def get_team_form(self, team_data):
        if 'form' not in team_data or not team_data['form']:
            logger.warning("No form data available")
            return "Not available"
        
        form = team_data['form']
        logger.debug(f"Team form: {form}")
        return form