
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
"questStatus": "not started",
"inventory": [""]
},
"status": {
"morale": 100,
"emotion": "",
"reason": "",
"goals": [""]
},
"custom": {
"favoriteColor": "",
"hometown": "",
"fears": [""],
"memories": [],
"quirk":[],
"secrets":[],
"affect":[],
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
    prompt = '''You write paragraphs from game characters describing themselves in the first person. 
    The following is a JSON file of information on the character, 
    output a paragraph to help the user decide whether to use this character. 
    Use drama and evocatve language to communicate the idea of the character instead if just listing out facts, imply instead of say. 
    Only say what the character would tell a stranger, do not tell secrets.\n\n\n''' + f"{Character_JSON}\n\nInsert description here: "

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

    
def imagine_character(Seed="Agatha the Fearless Warrior"):
    prompt = f'Here are 2 characters for a game in the format <name> the <adjective> <ocupation>:\n{Seed}\n'

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
#start_chat("""You are an AI Actor in a videogame portraying characters that are sent to you. You will produce dialog on behalf of the character.""")
#description = input("Enter Description: ")
#character = create_character(description)
#summary = summarize_character(character)
#print(summary)

idea=imagine_character()
print(idea)
