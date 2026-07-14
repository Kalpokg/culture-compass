from dotenv import load_dotenv
import os

load_dotenv()

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
TICKETMASTER_API_SECRET = os.getenv("TICKETMASTER_API_SECRET")