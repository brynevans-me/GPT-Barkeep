import Conversations
from Conversations import imagine_character
from Conversations import create_character
from Conversations import summarize_character
from Conversations import start_chat
import json

# OS and Env
import os
from dotenv import load_dotenv
load_dotenv()

#Other Files

# MongoDB Config
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['gtp_json']
characters_collection = db['characters']

# OpenAI Config
import openai
openai.api_key = os.getenv("API_KEY")

# TESTING SPACE
with open('EvelynPrime.json', 'r') as f:
    Evelyn = json.load(f)
#idea = summarize_character(Evelyn)
#print(idea)
with open('RP_SystemPrompt.txt', 'r') as file:
    RPSystem = file.read()
start_chat(RPSystem)
