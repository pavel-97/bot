from utility import HotelRequest
from models import History
from dotenv import load_dotenv
import os


BASE_DIR = os.getcwd()
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

TOKEN = os.getenv('TOKEN')

bot = HotelRequest(token=TOKEN)
History.create_table()
