from pathlib import Path

# projektets rot
PROJECT_ROOT = Path(__file__).parent.parent

#directory till logs
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# api config, behövs skyddas 
API_KEY = "ae048f6fa27a448cad56f41748b7c0ae"
API_URL = "https://api.football-data.org/v4/competitions/PL/standings"

LOG_FILE = LOGS_DIR / "project.log"