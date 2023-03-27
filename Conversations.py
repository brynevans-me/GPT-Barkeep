
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

#JSON Config
import json

def start_chat(SystemCommand):
    # Initialize the list of messages with a system message
    messages = [
        {"role": "system", "content": f"{SystemCommand}"},
    ]

    # Set the parameters for the GPT-3 API request
    model = "gpt-3.5-turbo"
    temperature = 0.7

    # Start the conversation loop
    while True:
        # Get the user input
        user_input = input("User: ")

        # Check if the user wants to exit the conversation
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Assistant: Goodbye!")
            break

        # Add the user input to the messages list
        messages.append({"role": "user", "content": user_input})

        # Generate a response using the GPT-3 chat model
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=temperature,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the generated response and print it
        generated_response = response.choices[0].message['content']
        print(f"Assistant: {generated_response}")

        # Add the assistant's response to the messages list
        messages.append({"role": "assistant", "content": generated_response})
def create_character(CharacterDescription):
    prompt = '''You generate characters for an RPG. The format is as follows:

{
"characterID": "AI12345",
"basicInfo": {
"name": "",
"gender": "",
"occupation": "",
"age": 
},
"appearance": {
"hairColor": "",
"eyeColor": "",
"height": ""
},
"personality": {
"moralAlignment": [""],
"traits": [""],
"likes": [""],
"dislikes": [""]
},
"relationships": {
"friends": [""],
"romantic": [""],
"family": [""],
"enemies": [""]
},
"gameSpecific": {
"faction": "",
"inventory": [""]
},
"status": {
"morale": 100,
"emotion": "",
"reason": "",
"longtermgoals": [""]
"shorttermgoals": [""]
},
"custom": {
"favoriteColor": "",
"hometown": "",
"fears": [""],
"memories": [""],
"quirks":[""],
"secrets":[""],
"affect":[""],
"knowledge":[""]
} 

Based on the character description generate a matching JSON file. Invent details, name, relationships, etc. Anything not passed by the prompt should be invented. Some characters may need fields not listed in the example. Invent information not provided in the prompt to flesh out the character including names and places. Characters should be flawed but people. They should have pastimes and interests outside of their archetype. They should have non-mission related goals like normal humans. They should like things that would make a person like them happy. Every character should have something weird about them. Every character should have a secret and a unique way of speaking. Only output JSON. 

Factions are "Soldier","Peasant","Noble","Bandit","Evil","Animal"

Character Description: ''' + f"{CharacterDescription}.\n\nBegin JSON:\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    generated_text = response.choices[0].text.strip()

    try:
        character_json = json.loads(generated_text)
    except json.JSONDecodeError:

        print(f"{generated_text}\n\n")
        print("Error: Unable to parse the generated JSON")
        character_json = None

    return character_json
def summarize_character(Character_JSON):
    prompt = '''Use  one sentence to complete this prompt. Don't give too much information, just what someone looking would see: 
I am a bartender. As I finish polishing up a glass I look up and see the following character sitting in a  stool:\n\n''' + f"{Character_JSON}\n\nWhen I look at them I see: "

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    generated_text = response.choices[0].text.strip()


    return generated_text    
def imagine_character(Seed="Medieval",Num=1):
    #Num = Num + 1
    prompt = f'Here are {Num} characters for a {Seed} game in the format \n<name> the <adjective> <occupation>\n<name> the <adjective> <occupation>\n'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.8,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    generated_text = response.choices[0].text.strip()
 
    return generated_text

