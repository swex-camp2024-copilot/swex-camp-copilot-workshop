import os

import openai

from bot.player import PlayerBot


class HrvojeAndLorenzosUnbeatablePlayer(PlayerBot):
    API_KEY = os.getenv("OPENAI_API_KEY")

    def __init__(self):
        super().__init__()
        # create openai instance with api key
        self.openai = openai.OpenAI(api_key=self.API_KEY)
        self.character = ""
        self.ask_history = ""
        self.name = "Hrvoje and Lorenzo's Unbeatable Player"

    def choose_character(self) -> str:
        # Open a chat and ask a prompt
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a machine that chooses a celebrity and only answers with name and surname."},
                {"role": "user", "content": "Choose a lesser known celebrity who is a blonde woman."},
            ],
        )
        # Extract the assistant's reply
        self.character = response['choices'][0]['message']['content']
        return self.character

    def ask_question(self, query: str) -> str:
        # Open a chat and ask a question
        self.ask_history += query + "\n"
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a machine trying to guess a celebrity."
                                              "The guessing provided in each prompt."
                                              "Ask yes or no questions to narrow down the possibilities."
                                              "Guess the celebrity with name and surname only when your choice is narrowed down to a single person."
                                              "Try to make questions in such a way that you can eliminate as many people as possible."
                                              "Your output should be a single yes or no question."},
                {"role": "user", "content": self.ask_history},
            ],
        )
        return response['choices'][0]['message']['content']

    def respond(self, query: str) -> str:
        # Open a chat and ask a question
        response = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a machine that is impersonating {self.character}."
                                              f"You answer to questions only with yes or no."
                                              f"Under no circumstances should you answer with anything other than yes or no"},
                {"role": "user", "content": query},
            ],
        )
        return response['choices'][0]['message']['content']

    def reset(self) -> None:
        self.ask_history = ""
        self.character = ""
