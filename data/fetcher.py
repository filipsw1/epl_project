import requests
from config.settings import API_KEY, API_URL
from utils.logger import get_logger

logger = get_logger()

def fetch_table():

    # hämta epl tabellen från API
    logger.info("Fetching the EPL table data from API...")

    headers = {
        "X-Auth-Token": API_KEY
    }

    # försöker hämta datan, kastar exception vid fel 
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()

        logger.info("Successfully fetched EPL table data")
        return response.json()
    
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        raise

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occured: {e}")
        raise

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data: {e}")
        raise