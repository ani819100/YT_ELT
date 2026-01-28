import json
from datetime import date
import logging

logger = logging.getLogger(__name__)

def load_data():
    file_path = f"./data/YT_data_{date.today()}.json"

    try:
        logger.info(f"Processing file")
        with open(file_path, 'r',encoding='utf-8') as raw_data:
            data = json.load(raw_data)
        return data
    except FileNotFoundError:
        logger.error("File not found")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON file")
        raise
        