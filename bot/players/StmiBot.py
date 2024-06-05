import os
from openai import OpenAI
from bot.player import PlayerBot

class StmiBot(PlayerBot):

    def __init__(self):
        super().__init__("StmiBot")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.messages = []

    def choose_character(self):
        # Use OpenAI to generate a character name
        response = self.client.completions.create(model="gpt-3.5-turbo-instruct", prompt="Create a full name of character that is a real person or fantasy person", max_tokens=60)
        return response.choices[0].text.strip()

    def ask_question(self, query):
        # If the query is None, ask the initial question about character
        if query is None:
            response = self.client.completions.create(model="gpt-3.5-turbo-instruct", prompt="Ask a question to guess about character", max_tokens=60)
            return response.choices[0].text.strip()
        # Use OpenAI to generate a question
        self.messages.append(query)
        response = self.client.completions.create(model="gpt-3.5-turbo-instruct", prompt=self.messages, max_tokens=60)
        return response.choices[0].text.strip()

    def respond(self, query):
        # Use OpenAI to generate a response
        response = self.client.completions.create(model="gpt-3.5-turbo-instruct", prompt=query, max_tokens=60)
        return response.choices[0].text.strip()

    def reset(self):
        self.messages = []          
    