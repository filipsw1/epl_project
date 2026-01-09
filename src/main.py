from data.fetcher import fetch_table, fetch_matches
from analysis.table_filter import TableFilter
from config.settings import FORM_COLORS, POSITION_COLORS
from utils.logger import get_logger

logger = get_logger()

# matchform för lagen, vinst = grön, förlust = röd, lika = grå
def format_form(form_string):
    if not form_string or form_string == "Not available":
        return "N/A"
    
    colored_form = ""
    for char in form_string:
        if char == 'W':
            colored_form += f"{FORM_COLORS['W']}W{FORM_COLORS['RESET']}"
        elif char == 'L':
            colored_form += f"{FORM_COLORS['L']}L{FORM_COLORS['RESET']}" 
        elif char == 'D':
            colored_form += f"{FORM_COLORS['D']}D{FORM_COLORS['RESET']}" 
        else:
            colored_form += char
    
    return colored_form

# tabell header
def print_table_header():
    print("\n" + "‾"*90)
    print(f"{'Pos':<4} {'Team':<30} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<4} {'GA':<4} {'GD':<4} {'Pts':<4} {'Form':<15}")
    print("\n" + "‾"*90)


def print_team_row(team, table_filter=None, matches_data=None, show_form=True):

    pos = team['position']
    name = team['team']['name']
    played = team['playedGames']
    won = team['won']
    draw = team['draw']
    lost = team['lost']
    gf = team['goalsFor']
    ga = team['goalsAgainst']
    gd = team['goalDifference']
    pts = team['points']

    if matches_data and table_filter:
        form_str = table_filter.calculate_form(team['team']['id'], matches_data)
        form_display = format_form(form_str)
    else:
        form_display = "N/A"
    
    if 1 <= pos <= 4:
        bg_color = POSITION_COLORS['CL']
    elif 5 <= pos < 6:
        bg_color = POSITION_COLORS['EL']
    elif 18 <= pos <= 20:
        bg_color = POSITION_COLORS['REL']
    else:
        bg_color = ""
    
    reset = POSITION_COLORS['RESET'] if bg_color else ""
    if show_form:
        print(f"{bg_color}{pos:<4} {name:<30} {played:<3} {won:<3} {draw:<3} {lost:<3} {gf:<4} {ga:<4} {gd:<4} {pts:<4}{reset} {form_display:<15}")
    else:
        print(f"{bg_color}{pos:<4} {name:<30} {played:<3} {won:<3} {draw:<3} {lost:<3} {gf:<4} {ga:<4} {gd:<4} {pts:<4}{reset}")

def display_full_table(table_filter, matches_data=None):  
    logger.info("Displaying full table")
    print("\n" + "="*90)
    print("PREMIER LEAGUE TABLE 2025/26".center(90))
    print_table_header()
        
    for team in table_filter.get_full_table():
        print_team_row(team, table_filter, matches_data)
  
    print("="*90)

    print(f"\n{POSITION_COLORS['CL']}  {POSITION_COLORS['RESET']} Champions League (1-4)   "
          f"{POSITION_COLORS['EL']}  {POSITION_COLORS['RESET']} Europa League (5)   "
          f"{POSITION_COLORS['REL']}  {POSITION_COLORS['RESET']} Relegation (18-20)")
    return_to_menu()

def search_team(table_filter, matches_data=None):
    logger.info("User searched for a team")
    
    # input
    team_name = input("\nEnter team name: ").strip()
    
    if not team_name:
        logger.warning("Empty team name provided")
        print("Team name cannot be empty!")
        return
    
    if len(team_name) < 2:
        logger.warning("Team name too short")
        print("Team name must be at least 2 characters!")
        return
    
    team = table_filter.get_team_by_name(team_name)
    
    if team:
        print("\n" + "="*90)
        print(f"TEAM: {team['team']['name']}".center(90))
        print_table_header()
        print_team_row(team, table_filter, matches_data)
        print("="*90)
        
        # andra stats
        home = team.get('home', {})
        away = team.get('away', {})
        if home:
            print(f"   Home record: {home.get('won', 0)}W - {home.get('draw', 0)}D - {home.get('lost', 0)}L")
        if away:
            print(f"   Away record: {away.get('won', 0)}W - {away.get('draw', 0)}D - {away.get('lost', 0)}L")
        
        # 5 senaste resultaten
        if matches_data:
            team_id = team['team']['id']
            all_matches = matches_data.get('matches', [])
            
            team_matches = [m for m in all_matches 
                            if m['homeTeam']['id'] == team_id or m['awayTeam']['id'] == team_id]
            
            team_matches.sort(key=lambda x: x['utcDate'])
            
            finished_matches = [m for m in team_matches if m['status'] == 'FINISHED']
            
            last_5 = finished_matches[-5:] if len(finished_matches) >= 5 else finished_matches
            last_5.reverse()
            
            print(f"\nLast {len(last_5)} Results:")
            for match in last_5:
                home_team = match['homeTeam']['shortName']
                away_team = match['awayTeam']['shortName']
                home_score = match['score']['fullTime']['home']
                away_score = match['score']['fullTime']['away']
                date = match['utcDate'][:10]
                
                print(f"   {home_team} vs {away_team} {home_score}-{away_score} - {date}")
        
    else:
        print(f"\n Team '{team_name}' not found!")
    return_to_menu()


def display_menu():
    print("EPL PROJECT".center(50))
    print("="*50)
    print("1. View Premier League Standings")
    print("2. Search for Premier League Team")
    print("3. Exit")

def return_to_menu():
    input("\nClick 'Enter' to return to menu\n")

def get_user_choice():

    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if not choice:
                print("Please enter a number!")
                continue
            
            choice_int = int(choice)
            
            if 1 <= choice_int <= 3:
                return choice_int
            else:
                print("Invalid choice! Please enter a number between 1-3.")
                
        except ValueError:
            logger.warning(f"Invalid input received: {choice}")
            print("Invalid input! Please enter a number between 1-3.")


def main():
    logger.info("EPL Project started")
    
    try:    
        print("\nFetching Premier League data...")
        data = fetch_table()
        
        matches_data = fetch_matches()

        table_filter = TableFilter(data)
        
        while True:
            display_menu()
            choice = get_user_choice()
            
            if choice == 1:
                display_full_table(table_filter, matches_data)
            elif choice == 2:
                search_team(table_filter, matches_data)
            elif choice == 3:
                print("\nThank you for using EPL Project!")
                logger.info("Program exited by user")
                break
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n An error occurred: {e}")
    finally:
        logger.info("EPL Project ended")
        print()


if __name__ == "__main__":
    main()