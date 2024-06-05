from player import PlayerBot
from openai import OpenAI


class WisaOnanPlayerBot(PlayerBot):
    def __init__(self):
        super().__init__('Concrete Player')
        self.history = []  # Add this line to initialize the list
        self.secret_character = None
        self.client = OpenAI()

    def choose_character(self) -> str:
        self.secret_character = self.create_completion_choose_character('gpt-4', 'Generate a character name')

    def ask_question(self, query: str) -> str:
        if query is not None:
            self.history.append("answer:" + query)
        question_prompt = "Either ask a question to guess the character. or if you are ready to guess do so."
        prompt = "Game history:" + "\n".join(self.history) + "\n\n" + question_prompt
        question = self.create_completion_guesser('gpt-4', prompt)
        self.history.append("question:" + question)
        return question

    def respond(self, query: str) -> str:
        prompt = f"Given that the secret character is {self.secret_character}, answer the following yes/no question: {query}"
        response = self.create_completion_respond('gpt-4', prompt)
        return 'yes' if 'yes' in response.lower() else 'no'

    def reset(self) -> str:
        self.history = []
        self.secret_character = None

    def create_completion_guesser(self, model, prompt):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": """
                 You are playing a game where you have to guess the secret character chosen by your opponent.
                  You can ask yes/no questions to figure out who the character is.
                  When you're ready to make a guess, say 'I know the character is [character name]'."""},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def create_completion_choose_character(self, model, prompt):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": """You are a creative AI.
                  That Generates a secret character for a guessing game.
                   The character should be from a well-known book, movie, or TV show.
                   You only respond with the character name"""
                 },
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    def create_completion_respond(self, model, prompt):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system",
                 "content": """
                 You are an AI in a guessing game. You know the secret character. 
                 Your role is to answer yes/no questions about the character without revealing their identity.
                 """},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
