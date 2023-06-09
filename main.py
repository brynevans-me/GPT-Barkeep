import json
import openai
import os
# OS and Env
import os
from Conversations import create_character
from Conversations import start_chat
from Conversations import imagine_character
from dotenv import load_dotenv
load_dotenv()

# set up OpenAI API
openai.api_key = os.getenv("API_KEY")

# valid occupations
occupations = {
    "doctor": "Doctor",
    "lawyer": "Lawyer",
    "teacher": "Teacher",
    "engineer": "Engineer",
    "artist": "Artist"
}

# valid hair, eye, and skin colors
hair_colors = ["black", "blonde", "brown", "red", "grey", "white", "auburn", "caramel", "chestnut", "platinum",
               "strawberry blonde", "dirty blonde", "golden blonde", "honey blonde", "light brown", "dark brown",
               "copper", "mahogany", "burgundy", "russet", "jet black", "midnight blue", "dark green", "purple", "pink",
               "silver", "steel grey", "ash blonde", "champagne blonde", "beige blonde", "blonde"]
eye_colors = ["amber", "blue", "brown", "gray", "green", "hazel", "black", "chocolate"]
skin_colors = ["fair", "light", "medium", "olive", "brown", "dark", "ebony", "white", "black", "tan"]


# Game introduction
def game_intro():
    # ASCII art of a fantasy tavern
    print("""
                                                     ___
                                             ___..--'  .`.
                                    ___...--'     -  .` `.`.
                           ___...--' _      -  _   .` -   `.`.
                  ___...--'  -       _   -       .`  `. - _ `.`.
           __..--'_______________ -         _  .`  _   `.   - `.`.
        .`    _ /\    -        .`      _     .`__________`. _  -`.`.
      .` -   _ /  \_     -   .`  _         .` |__Ye_Olde__|`.   - `.`.
    .`-    _  /   /\   -   .`        _   .`   |__Tavern___|  `. _   `.`.
  .`________ /__ /_ \____.`____________.`     ___       ___  - `._____`|
    |   -  __  -|    | - |  ____  |   | | _  |   |  _  |   |  _ |
    | _   |  |  | -  |   | |.--.| |___| |    |___|     |___|    |
    |     |--|  |    | _ | |'--'| |---| |   _|---|     |---|_   |
    |   - |__| _|  - |   | |.--.| |   | |    |   |_  _ |   |    |
 ---``--._      |    |   |=|'--'|=|___|=|====|___|=====|___|====|
 -- . ''  ``--._| _  |  -|_|.--.|_______|_______________________|
`--._           '--- |_  |:|'--'|:::::::|:::::::::::::::::::::::|
_____`--._ ''      . '---'``--._|:::::::|:::::::::::::::::::::::|
----------`--._          ''      ``--.._|:::::::::::::::::::::::|
`--._ _________`--._'        --     .   ''-----.................'
     `--._----------`--._.  _           -- . :''           -    ''
          `--._ _________`--._ :'              -- . :''      -- . ''
 -- . ''       `--._ ---------`--._   -- . :''
          :'        `--._ _________`--._:'  -- . ''      -- . ''
  -- . ''     -- . ''    `--._----------`--._      -- . ''     -- . ''
                              `--._ _________`--._
 -- . ''           :'              `--._ ---------`--._-- . ''    -- . ''
          -- . ''       -- . ''         `--._ _________`--._   -- . ''
:'                 -- . ''          -- . ''  `--._----------`--._
        """)
    print("Welcome to RPG Tavern Simulator!")
    print(
        "You find yourself at the entrance of a bustling tavern, where weary adventurers gather to unwind after quests.")
    print("As you approach the door, you catch a glimpse of your reflection in the tavern window.")
    print("You examine your features...")


# function to validate user input
def validate_input(prompt, valid_inputs):
    valid_choice = False
    while not valid_choice:
        user_input = input(prompt).lower()
        if user_input in valid_inputs:
            valid_choice = True
            return user_input
        else:
            print("Invalid choice. Please try again.")


# function to create a character
def create_player1():
    if os.path.exists("Player1.json"):
        with open("Player1.json", "r") as f:
            existing_character = json.load(f)

        print("\nYou have an existing character saved!")
        print(f"Name: {existing_character['name']}")
        print(f"Gender: {existing_character['gender']}")
        print(f"Occupation: {existing_character['occupation']}")
        print(f"Age: {existing_character['age']}")
        print(f"Hair Color: {existing_character['hair_color']}")
        print(f"Eye Color: {existing_character['eye_color']}")
        print(f"Skin Color: {existing_character['skin_color']}")
        print(f"Height: {existing_character['height']} {existing_character['height_unit']}")

        valid_choice = False
        while not valid_choice:
            confirm = input("Is this you? (y/n): ")
            if confirm.lower() == "y":
                return existing_character
            elif confirm.lower() == "n":
                confirm_delete = input(
                    "Are you sure you want to delete this character and create a new one? This cannot be undone. (y/n): ")
                if confirm_delete.lower() == "y":
                    os.remove("Player1.json")
                    break
                else:
                    valid_choice = True
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

    print("Let's create your character!")

    # ask user for measurement system
    valid_choice = False
    while not valid_choice:
        measurement = input("Will you be using metric or imperial units? (m/i): ")
        if measurement.lower() == "m":
            height_unit = "meters"
            weight_unit = "kg"
            valid_choice = True
        elif measurement.lower() == "i":
            height_unit = "inches"
            weight_unit = "lbs"
            valid_choice = True
        else:
            print("Invalid choice. Please enter 'm' for metric or 'i' for imperial.")

    # ask user for character traits
    valid_age = False
    while not valid_age:
        try:
            age = int(input("Enter age: "))
            if age < 1 or age > 130:
                print("Invalid age. Please enter a value between 1 and 130.")
            else:
                valid_age = True
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    valid_height = False
    while not valid_height:
        try:
            height = float(input(f"Enter height in {height_unit}: "))
            if measurement.lower() == "m" and (height < 0.5 or height > 2.5):
                print("Invalid height. Please enter a value between 0.5 and 2.5 meters.")
            elif measurement.lower() == "i" and (height < 20 or height > 100):
                print("Invalid height. Please enter a value between 20 and 100 inches.")
            else:
                valid_height = True
        except ValueError:
            print("Invalid input. Please enter a valid decimal.")

    name = input("Enter character name: ")

    gender = validate_input("Enter gender (male/female/non-binary): ", ["male", "female", "non-binary"])

    occupation = validate_input("Enter occupation (doctor/lawyer/teacher/engineer/artist): ", occupations)

    hair_color = validate_input("Enter hair color: ", hair_colors)

    eye_color = validate_input("Enter eye color: ", eye_colors)

    skin_color = validate_input("Enter skin color: ", skin_colors)

    # print character traits for confirmation
    print("\nYou examine the reflection in the Tavern window... ")
    print(f"Name: {name}")
    print(f"Gender: {gender}")
    print(f"Occupation: {occupations[occupation]}")
    print(f"Age: {age}")
    print(f"Hair Color: {hair_color}")
    print(f"Eye Color: {eye_color}")
    print(f"Skin Color: {skin_color}")
    print(f"Height: {height} {height_unit}")

    # ask user for confirmation
    valid_confirm = False
    while not valid_confirm:
        confirm = input("Is this you? (y/n): ")
        if confirm.lower() == "y":
            valid_confirm = True
        elif confirm.lower() == "n":
            # ask user for corrected character traits
            failed_inputs = []
            if age < 1 or age > 130:
                failed_inputs.append("age")
                print("Invalid age. Please enter a value between 1 and 130.")
            if measurement.lower() == "m" and (height < 0.5 or height > 2.5):
                failed_inputs.append("height")
                print("Invalid height. Please enter a value between 0.5 and 2.5 meters.")
            elif measurement.lower() == "i" and (height < 20 or height > 100):
                failed_inputs.append("height")
                print("Invalid height. Please enter a value between 20 and 100 inches.")
            if gender.lower() not in ["male", "female", "non-binary"]:
                failed_inputs.append("gender")
                print("Invalid gender. Please enter 'male', 'female', or 'non-binary'.")

            name = input("Enter character name: ")
            occupation = validate_input("Enter occupation (doctor/lawyer/teacher/engineer/artist): ", occupations)
            hair_color = validate_input("Enter hair color: ", hair_colors)
            eye_color = validate_input("Enter eye color: ", eye_colors)
            skin_color = validate_input("Enter skin color: ", skin_colors)

            # print character traits for confirmation
            print("\nConfirm your character traits:")
            print(f"Name: {name}")
            print(f"Gender: {gender}")
            print(f"Occupation: {occupations[occupation]}")
            print(f"Age: {age}")
            print(f"Hair Color: {hair_color}")
            print(f"Eye Color: {eye_color}")
            print(f"Skin Color: {skin_color}")
            print(f"Height: {height} {height_unit}")

            # ask user for confirmation
            confirm_failed = False
            while not confirm_failed:
                confirm = input("Is this information correct? (y/n): ")
                if confirm.lower() == "y":
                    valid_confirm = True
                    confirm_failed = True
                elif confirm.lower() == "n":
                    confirm_failed = True
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    # create character dictionary
    character = {
        "name": name,
        "gender": gender,
        "occupation": occupations[occupation],
        "age": age,
        "hair_color": hair_color,
        "eye_color": eye_color,
        "skin_color": skin_color,
        "height": height,
        "height_unit": height_unit,
        "weight_unit": weight_unit,
        "inventory": [],
        "quest": "",
        "quest_status": "",
        "aura": ""
    }

    # save character as JSON file
    with open("Player1.json", "w") as f:
        json.dump(character, f)

    print("Character created and saved!")
    return character


def entering_tavern():
    # Describe the interior of the tavern
    print(
        "You push open the heavy wooden doors and step into a dimly lit room. The air is thick with the smells of smoke, ale, and roasting meat. The tavern is packed with people, and the noise level is deafening. You can hear the sound of dice being rolled, the clatter of tankards, and the occasional burst of laughter.")
    # Offer the player a choice of actions
    print("What would you like to do?")
    print("1. Approach the bar")
    print("2. Look for someone to talk to")
    print("3. Find a table to sit down at")
    choice = input("Enter your choice (1-3): ")
    # Handle the player's choice
    if choice == "1":
        # Describe the bar area and the barkeep
        print(
            "You push your way through the crowd and make your way to the bar. The barkeep is a grizzled old man with a bushy beard and a scowl. He's polishing a mug with a rag, and he looks up as you approach.")
        approach_bar()
    elif choice == "2":
        look_for_someone()
    elif choice == "3":
        find_table()
    else:
        print("Invalid choice. Please try again.")
        entering_tavern()  # call the function again to give the player another chance to make a choice

def approach_bar():
    """
    This function describes the player approaching the bar, interacting with the barkeep, and choosing a course of action.
    """
    # Barkeep dialogue
    print("Barkeep: What can I get for ya? We've got ale, mead, and some stronger stuff if you're feelin' adventurous.")
    # Offer the player a choice of actions
    print("What would you like to do?")
    print("1. Chat with the barkeep")
    print("2. Order a drink")
    print("3. Order some food")
    print("4. Look around the bar")
    print("5. Leave the bar")
    choice = input("Enter your choice (1-5): ")
    # Handle the player's choice
    if choice == "1":
        initiate_chat_barkeep()
    elif choice == "2":
        print("You order a drink from the barkeep. He pours you a mug of ale and slides it across the counter to you.")
        entering_tavern()
    elif choice == "3":
        print("You order some food from the barkeep. He grumbles and disappears into the kitchen, but returns a few minutes later with a plate of greasy sausages and potatoes.")
        entering_tavern()
    elif choice == "4":
        print("You take a moment to look around the bar and examine the other patrons.")
        generated_characters = imagine_character("Medieval", 4).split("\n")
        print("\nThe people at the bar include:")
        for i, character in enumerate(generated_characters):
            print(f"{i + 1}. {character}")
        print(f"{len(generated_characters) + 1}. Go back")
        selection = input("Enter the number of the person you want to talk to: ")
        if selection.isnumeric() and int(selection) in range(1, len(generated_characters) + 1):
            character = create_character(generated_characters[int(selection) - 1])
            with open("character.json", "w") as f:
                json.dump(character, f)
            with open("RP_SystemPrompt.txt", "r") as f:
                system_prompt = f.read()
            with open("character.json", "r") as f:
                character_json = json.load(f)
            character_description = system_prompt + "\n" + json.dumps(character_json) + "\n" + "{{the player sits next to you at the bar and looks to you as if to start a conversation}}"
            start_chat(character_description)
        elif selection == str(len(generated_characters) + 1):
            entering_tavern()
        else:
            print("Invalid choice. Please try again.")
            approach_bar()
    elif choice == "5":
        print("You decide to leave the bar and explore the rest of the tavern.")
        entering_tavern()
    else:
        print("Invalid choice. Please try again.")
        approach_bar()
def initiate_chat_barkeep():
    """
    This function initiates a chat with GPT and allows the player to converse with a character.
    """
    with open('RP_SystemPrompt.txt', 'r') as file:
        system_prompt = file.read()

    with open('barkeep_001.json', 'r') as file:
        npc_json = file.read()

    string_of_text = "{{The player approaches the bar and greets you}}"

    concatenated_text = system_prompt + "\n" + npc_json + "\n" + string_of_text
    start_chat(concatenated_text)
    approach_bar()



# test function
game_intro()
create_player1()
entering_tavern()
