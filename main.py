
import os
from dotenv import load_dotenv
from InternetSpeedTwitterBot import Bot

load_dotenv()

client_id = os.getenv("CLIENT_ID")
consumer_key=os.getenv('API_KEY')
consumer_secret=os.getenv('API_KEY_SECRET')
access_token=os.getenv('ACCESS_TOKEN')
access_token_secret=os.getenv('ACCESS_TOKEN_SECRET')



bot=Bot(consumer_key,consumer_secret,access_token,access_token_secret,client_id)

bot.get_internet_speed()





