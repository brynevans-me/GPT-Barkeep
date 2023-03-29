
# OS and Env
import os
from dotenv import load_dotenv
load_dotenv()

#Other Files

# MongoDB Config
from pymongo import MongoClient
from bson import ObjectId
client = MongoClient('mongodb://localhost:27017/')
db = client['gtp_json']
characters_collection = db['characters']

# OpenAI Config
import openai
openai.api_key = os.getenv("API_KEY")

#JSON Config
import json

def store_character(character_json):
    if character_json:
        insert_result = characters_collection.insert_one(character_json)
        return character_json["characterID"]
    else:
        return None
def get_character_by_id(character_id):
    character_data = characters_collection.find_one({"characterID": character_id})
    return character_data
def update_character(character_id, updated_data):
    characters_collection.update_one({"characterID": character_id}, {"$set": updated_data})
def list_all_character_names():
    character_names = []

    for character in characters_collection.find():
        char_id = str(character["_id"])
        name = character["basicInfo"]["name"]
        character_names.append((char_id, name))

    return character_names
def start_chat(character_id, system_command="""
You are an AI Actor in a videogame portraying characters that are sent to you. You will produce dialog on behalf of the character.

Do not narrate anything other than direct character actions such as *removes hat* or *shakes hand*. Keep your responses as concise as possible. The player will act opposite you filling in the hero's dialog. Please respond to their statements and pursue your character's goals.

Please show the character's thoughts and internal reasoning in [[]] brackets.

Any information delivered in JSON Notation or {{}} comes from the overworld. Plain text is player input.
"""):
    character_data = get_character_by_id(character_id)
    if not character_data:
        print("Error: Character not found")
        return

    # Initialize the list of messages with a system message
    messages = [
        {"role": "system", "content": f"{system_command}\n{character_data}"},
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
            
            # Add the user input to the messages list
            messages.append({"role": "user", "content": "Modify the original JSON data to represent this player interaction. Be extreme with your changes, I want the character to seem to remember this interaction. Feel free to add any categories to the JSON you think would help. Reset the goals based off information and changes in this session, make the character dynamic but consistent."})

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

            # Extract the generated response and update the character data
            updated_character_data = json.loads(response.choices[0].message['content'])
            update_character(character_id, updated_character_data)
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
def new_character():
    while True:
        user_input = input("Do you want to provide a character description or have one generated? (provide/generate): ")
        if user_input.lower() == "provide":
            character = input("Enter your character description: ")
            break
        elif user_input.lower() == "generate":
            type = input("Enter a type (or press Enter for Medieval): ")
            type = type if type != "" else None
            print("Imagining a character")
            character = imagine_character(Seed=type)
            print(f"What about {character}")
            user_input = input("Create this character? (y/n): ")
            if user_input.lower() == "y":
                break
        else:
            print("Invalid input. Please enter 'provide' or 'generate'.")

    characterJson = create_character(character)
    characterSummary = summarize_character(characterJson)
    print(f"\n\n\n-------------------\n{character}\n-------------------\n")
    print(characterSummary)
    user_input = input("\n\nDo you want to create this character? [y/n] ")
    if user_input.lower() == "y":
        character_id = store_character(characterJson)
        return character_id
def list_characters():
    return list(characters_collection.find())
def delete_character(character_id):
    result = characters_collection.delete_one({"_id": ObjectId(character_id)})
    return result.deleted_count > 0
def get_character_by_id(character_id):
    return characters_collection.find_one({"_id": ObjectId(character_id)})
def manage_characters():
    while True:
        print("\nCharacter management:")
        print("1. List all characters")
        print("2. Delete a character")
        print("3. Load a character")
        print("4. Create a new character")
        print("5. Exit")
        user_input = input("Enter the number of your choice: ")

        if user_input == "1":
            character_names = list_all_character_names()
            for i, (char_id, name) in enumerate(character_names, start=1):
                print(f"{i}. {name} (ID: {char_id})")
        elif user_input == "2":
            character_id = input("Enter the character ID to delete: ")
            delete_character(character_id)
        elif user_input == "3":
            character_id = input("Enter the character ID to load: ")
            start_chat(character_id)
        elif user_input == "4":
            new_character()
            print("New character created.")
        elif user_input == "5":
            print("Exiting character management.")
            break
        else:
            print("Invalid input. Please try again.")
    while True:
        print("\n--- Manage Characters ---")
        print("1. List characters")
        print("2. Delete a character")
        print("3. Load a character")
        print("4. Exit")
        user_input = input("Choose an option (1-4): ")

        if user_input == "1":
            characters = list_characters()
            if characters:
                for i, character in enumerate(characters, start=1):
                    print(f"{i}. {character['basicInfo']['name']} (ID: {character['_id']})")
            else:
                print("No characters found in the database.")
        elif user_input == "2":
            character_id = input("Enter the ID of the character you want to delete: ")
            if delete_character(character_id):
                print("Character deleted successfully.")
            else:
                print("Character not found.")
        elif user_input == "3":
            character_id = input("Enter the ID of the character you want to load: ")
            character_data = get_character_by_id(character_id)
            if character_data:
                print(f"Character loaded: {character_data['basicInfo']['name']} (ID: {character_data['_id']})")
            else:
                print("Character not found.")
        elif user_input == "4":
            print("Exiting character management.")
            break
        else:
            print("Invalid input. Please choose an option between 1 and 4.")