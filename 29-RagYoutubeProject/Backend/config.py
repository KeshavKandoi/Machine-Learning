import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
