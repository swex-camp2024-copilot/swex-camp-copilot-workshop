import os

import openai
from openai.types.chat import ChatCompletion

from bot.player import PlayerBot


class HrvojeAndLorenzosUnbeatablePlayer(PlayerBot):

    def __init__(self):
        super().__init__("Hrvoje and Lorenzo's Unbeatable Player")
        # create openai instance with api key
        self.openai = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.character = ""
        self.ask_history = ""

    def choose_character(self) -> str:
        # Open a chat and ask a prompt
        completion: ChatCompletion = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a machine that chooses a celebrity and only answers with name and surname."},
                {"role": "user", "content": "Choose a lesser known celebrity who is a blonde woman."},
            ],
        )
        # Extract the assistant's reply
        self.character = completion.choices[0].message.content
        return self.character

    def ask_question(self, query: str) -> str:
        # Open a chat and ask a question
        self.ask_history += query + "\n"
        completion: ChatCompletion = self.openai.chat.completions.create(
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
        question = completion.choices[0].message.content
        self.ask_history += question + "\n"
        return question

    def respond(self, query: str) -> str:
        # Open a chat and ask a question
        completion: ChatCompletion = self.openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a machine that is impersonating {self.character}."
                                              f"You answer to questions only with yes or no."
                                              f"Under no circumstances should you answer with anything other than yes or no"},
                {"role": "user", "content": query},
            ],
        )
        return completion.choices[0].message.content

    def reset(self) -> None:
        self.ask_history = ""
        self.character = ""
