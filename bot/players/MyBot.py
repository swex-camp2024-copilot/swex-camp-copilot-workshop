import os
import openai
from bot.player import PlayerBot

class MyBot(PlayerBot):
    def __init__(self):
        super().__init__("MyBot")
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def choose_character(self):
        # Use OpenAI to generate a character name
        response = openai.Completion.create(engine="text-davinci-002", prompt="Character Name", max_tokens=60)
        return response.choices[0].text.strip()

    def ask_question(self, query):
        # Use OpenAI to generate a question
        response = openai.Completion.create(engine="text-davinci-002", prompt=query, max_tokens=60)
        return response.choices[0].text.strip()

    def respond(self, query):
        # Use OpenAI to generate a response
        response = openai.Completion.create(engine="text-davinci-002", prompt=query, max_tokens=60)
        return response.choices[0].text.strip()

    def reset(self):
        pass        
    