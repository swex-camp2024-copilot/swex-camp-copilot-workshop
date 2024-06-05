import os
from openai import OpenAI
from ..player import PlayerBot


class PapaFull(PlayerBot):
    def __init__(self, name):
        super().__init__(name)
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(
            api_key=self.api_key
        )
        self.chat_conversation_history = []

    def choose_character(self) -> str:
        pick_character_prompt = {
            "role": "system",
            "content": "you are participating in a game where you have to "
                       "guess the character of your opponent before he guesses "
                       "yours. To start the game you will be asked to pick a "
                       "real life character. You have to remember it and "
                       "answer questions about it until the game ends. It is "
                       "very important that you never tell lies and answer "
                       "honestly about your character. Now please pick a "
                       "character, remember it and return only its name"
        }
        return self.get_api_response(pick_character_prompt)

    def ask_question(self, query: str) -> str:
        ask_question_prompt = {
            "role": "user",
            "content": "it is your turn to try to guess the character of your opponent. You can ask any question that "
                       "can be answered with yes or no. You can ask as many questions as you want. When you think you "
                       "know the character you can make a guess. What is your question?"
        }
        return self.get_api_response(ask_question_prompt)

    def respond(self, query: str) -> str:
        respond_prompt = {
            "role": "user",
            "content": f"here is a question you have to answer. {query}? You have to answer honestly. You can only "
                       f"answer with yes or no. What is your answer?"
        }

        return self.get_api_response(respond_prompt)

    def reset(self) -> str:
        clean_up_state_prompt = {
            "role": "system",
            "content": "the game ended. now you have clean up the state of the game and prepare for next round"
        }

        return self.get_api_response(clean_up_state_prompt)

    def get_api_response(self, prompt):
        self.chat_conversation_history.append(prompt)
        response = self.client.chat.completions.create(
            messages=self.chat_conversation_history,
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content.strip()