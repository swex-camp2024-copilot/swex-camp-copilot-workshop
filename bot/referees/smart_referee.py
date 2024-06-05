import os
import openai
from bot.referee import RefereeBot

class SmartReferee(RefereeBot):
    def __init__(self):
        super().__init__("Smart Referee")
        openai.api_key = os.getenv("OPEN_AI_API_KEY")
        
    def set_character(self, name):
        self.character = name

    def validate_question(self, question):
        gptAnswer = self.askChatGPT(f"You should analyze players questions in 'Guess who am I' game. Player can either ask something about character or try to guess who the character is. Question: [{question}]. Is it a valid question for 'Guess who am I?' game? Please answer yes or no without interpunction.")
        if gptAnswer == "yes":
            gptAnswer = self.askChatGPT(f"You should analyze players questions in 'Guess who am I' game. Player can either ask something about character or try to guess who the character is. Question: [{question}]. Is the player trying to guess who the character is with this question? Please answer yes or no without interpunction.")
            if (gptAnswer == "yes"):
                gptAnswer = self.askChatGPT(f"Answer this question just by telling character name: [{question}].")
                if gptAnswer == self.character.lower():
                    return "CHARACTER_GUESSED"
                else:
                    return "CHARACTER_NOT_GUESSED"
            return "VALID"
        return "INVALID"

    def validate_answer(self, question, answer):
        gptAnswer = self.askChatGPT(f"I will provide you a question and an answer about the character. Question: [{question}] Answer: [{answer}] Character: [{self.character}]. Is the answer correct for the question? Please answer yes or no without interpunction.")
        if gptAnswer == "yes":
            return "VALID"
        return "INVALID"
    
    def askChatGPT(self, prompt):
          completion = openai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
              {
                "role": "user",
                "content": prompt,
              },
            ],
          )
          print("----------------------------------")
          print(f"Prompt: [{prompt}] Response: [{completion.choices[0].message.content}]")
          return completion.choices[0].message.content.lower()