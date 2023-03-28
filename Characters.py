import Conversations
import json

class Character:
    def __init__(self, name, description, json_data):
        self.name = name
        self.description = description
        self.json_data = json_data
    def display(self):
        print(f"Name: {self.name}")
        print(f"Description {self.description}")
        print(f"JSON:\n{self.json_data}")

