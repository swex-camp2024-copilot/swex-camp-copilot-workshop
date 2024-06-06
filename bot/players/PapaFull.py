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
        setup_prompt = {
            "role": "system",
            "content": "you are participating in a game where you have to guess the character of your opponent before "
                       "he guesses yours. It is a racing game which goes in separate rounds. Each round you must ask "
                       "only one question targeting the opposing character and you must provide only one answer "
                       "related to your character. To start the game must pick a secret character. You have to "
                       "remember it, keep it in secret and answer questions about it. The only answers you must "
                       "provide are strictly YES or NO. You must provide only one word as your answer. If the "
                       "question is not targeted to your character or is irrelevant,"
                       "answer with NO. Whenever you see the ASK_QUESTION token in any of the following prompts you "
                       "must ask your opponent exactly one question related to his character based on the information "
                       "you have gathered so far. If you dont have any context about the opposing character a good "
                       "starting question would be 'is your character male?' or 'is your character female?'. If you "
                       "already know who the opposing character is, you must guess its name. If you are not sure who "
                       "the opposing character is, ask specific question about it to deduct more information. Keep in "
                       "mind that the only possible answers you can get are YES or NO. You must structure your "
                       "questions so that you can deduct the most information out of them in the shortest amount of "
                       "rounds. Remember the answers and "
                       "use the information to tailor your next question about the opposing character so that you can "
                       "guess the character of your opponent in the shortest amount of rounds. Whenever you encounter "
                       "the ANSWER_QUESTION token in any of the following prompts it will always be followed by "
                       "exactly one question and it will be targeted to your character. You must answer the question "
                       "using only the available answers. Whenever you see the PICK_CHARACTER token in any of the "
                       "following prompts pick a character, keep it secret, remember it and only now, for the first "
                       "and last time, return only its name. Answer to this prompt with SETUP_COMPLETED to start "
                       "playing"
        }
        self.get_api_response(setup_prompt)

    def choose_character(self) -> str:
        pick_character_prompt = {
            "role": "system",
            "content": "PICK_CHARACTER"
        }
        return self.get_api_response(pick_character_prompt)

    def ask_question(self, query: str) -> str:
        if query is not None:
            self.chat_conversation_history.append({
                "role": "user",
                "content": f"{query}"
            })
        ask_question_prompt = {
            "role": "system",
            "content": "ASK_QUESTION"
        }
        return self.get_api_response(ask_question_prompt)

    def respond(self, query: str) -> str:
        respond_prompt = {
            "role": "user",
            "content": f"ANSWER_QUESTION {query}"
        }

        return self.get_api_response(respond_prompt)

    def reset(self) -> str:
        self.chat_conversation_history = []
        return "Papa Full has been reset."

    def get_api_response(self, prompt):
        self.chat_conversation_history.append(prompt)
        response = self.client.chat.completions.create(
            messages=self.chat_conversation_history,
            model="gpt-3.5-turbo",
        )
        res = response.choices[0].message.content.strip()
        self.chat_conversation_history.append({
            "role": "system",
            "content": res
        })
        return res
