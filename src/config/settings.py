from pathlib import Path

# projektets rot
PROJECT_ROOT = Path(__file__).parent.parent.parent

#directory till logs
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

try:
    from config.secrets import API_KEY
except ImportError:
    API_KEY = "INSERT_API_KEY_HERE"
API_URL = "https://api.football-data.org/v4/competitions/PL/standings"
API_MATCHES_URL = "https://api.football-data.org/v4/competitions/PL/matches"

LOG_FILE = LOGS_DIR / "project.log"

FORM_COLORS = {
    "W": "\x1b[32m", # grön
    "L": "\x1b[31m", # röd
    "D": "\x1b[90m", # grå
    "RESET": "\x1b[0m"
}

POSITION_COLORS = {
    "CL": "\033[48;5;22m",     
    "EL": "\033[48;5;94m",     
    "REL": "\033[48;5;52m",     
    "RESET": "\033[0m"
}
