from abc import ABC, abstractmethod


class PlayerBot(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def choose_character(self) -> str:
        pass

    @abstractmethod
    def ask_question(self, query: str) -> str:
        # Logic for making a decision based on the game state
        pass

    @abstractmethod
    def respond(self, query: str) -> str:
        # Logic for making a decision based on the game state
        pass

    @abstractmethod
    def reset(self):
        # Logic for making a decision based on the game state
        pass
