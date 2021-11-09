from utility import HotelRequest
from models import History
from dotenv import load_dotenv
import os
import logging


BASE_DIR = os.getcwd()
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '.env'))

TOKEN = os.getenv('TOKEN')

bot = HotelRequest(token=TOKEN)
History.create_table()

logging.basicConfig(filename='log_file.log', filemode='a+', format='%(name)s - %(levelname)s - %(message)s\n')
