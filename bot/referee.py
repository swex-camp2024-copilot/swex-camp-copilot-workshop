from abc import ABC, abstractmethod
from enum import Enum

from dotenv import load_dotenv


# this is enum for the game state
class ValidationResult(Enum):
    VALID = 1
    INVALID = 2
    CHARACTER_GUESSED = 3
    CHARACTER_NOT_GUESSED = 4


class RefereeBot(ABC):
    def __init__(self, name):
        load_dotenv()
        self.name = name
        self.character = ""

    @abstractmethod
    def set_character(self, name):
        pass

    @abstractmethod
    def validate_question(self, question: str) -> ValidationResult:
        pass

    @abstractmethod
    def validate_answer(self, question: str, answer: str) -> ValidationResult:
        # Logic for making a decision based on the game state
        pass
