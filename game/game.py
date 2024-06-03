class Game:
    def __init__(self, bot1, bot2):
        self.initializer = bot1
        self.guesser = bot2
        self.game_state = None
        self.last_response = None

    def initialize_game(self):
        character = self.initializer.choose_character()
        print(f"{self.initializer.name} chose {character}")

    def play_round(self, last_response=None):
        question = self.guesser.ask_question(query=last_response)
        print (f"{self.guesser.name}: {question}")
        response = self.initializer.respond(question)
        print(f"{self.initializer.name}: {response}")
        self.last_response = response
        return response

    def check_winner(self) -> bool:
        if not self.last_response:
            return False
        if "CORRECT" in self.last_response or "GAME OVER" in self.last_response:
            return True
        else:
            return False

    def update_game_state(self):
        # Logic for updating the game state
        pass