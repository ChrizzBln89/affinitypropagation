import os
import dotenv
from pathlib import Path

dotenv.load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("valuationhub")
CREDENTIALS = os.getenv("flash-realm-401106-a0bf29a37df7.json")

PATH_MAIN_DIR = str(Path(__file__).parent)
PATH_DATA_DIR = str(PATH_MAIN_DIR + "/data")

print(PROJECT_ID)
