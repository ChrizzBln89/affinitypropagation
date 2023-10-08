import os
import dotenv

dotenv.load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("valuationhub")
CREDENTIALS = os.getenv("flash-realm-401106-a0bf29a37df7.json")
