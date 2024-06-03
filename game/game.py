from time import sleep

from bot import referee
from bot.player import PlayerBot
from bot.referee import ValidationResult

INITIAL_SCORE = 25
EXCEPTION_PENALTY = 5
INVALID_QUESTION_PENALTY = 50
CHARACTER_NOT_GUESSED_PENALTY = 25
DISQUALIFICATION_PENALTY = 1000


class Game:
    def __init__(self, bot1: PlayerBot, bot2: PlayerBot, referees: list[referee]):
        self.bot1 = bot1
        self.bot2 = bot2
        self.referees = referees
        self.scores = {self.bot1: INITIAL_SCORE, self.bot2: INITIAL_SCORE}

    def play(self) -> PlayerBot:
        print("GAME STARTING " + self.bot1.name + " VS " + self.bot2.name)
        while self.scores[self.bot1] == self.scores[self.bot2]:
            self.reset_scores()
            self.play_rounds()
            if self.scores[self.bot1] == self.scores[self.bot2]:
                print("TIE BREAKER")

        return self.get_winner()

    def play_rounds(self):
        self.play_round(self.bot1, self.bot2)
        print("SWITCHING SIDES")
        self.play_round(self.bot2, self.bot1)
        self.print_scores()

    def play_round(self, answerer: PlayerBot, guesser: PlayerBot):
        secret_character = answerer.choose_character()
        print(answerer.name + " has selected the secret character:\n" + secret_character)
        self.set_character_for_referees(secret_character)
        response = None

        while self.scores[guesser] > 0:
            sleep(2)
            self.scores[guesser] -= 1
            question = self.ask_question(guesser, response)
            if question is None:
                continue
            print(guesser.name + ": " + question)

            validation_result = self.validate_question(question)
            if validation_result is not ValidationResult.VALID:
                self.handle_validation_result(guesser, validation_result)
                break

            sleep(2)
            response = self.get_answer(answerer, question)
            print(answerer.name + ": " + response)
            if response is None:
                continue
            if self.validate_answer(question, response) is ValidationResult.INVALID:
                self.scores[answerer] -= DISQUALIFICATION_PENALTY
                break

    def ask_question(self, guesser: PlayerBot, response: str) -> str:
        try:
            return guesser.ask_question(response)
        except Exception as e:
            print("OOPS SOMETHING WENT WRONG!")
            self.scores[guesser] -= EXCEPTION_PENALTY
            return None

    def get_answer(self, answerer: PlayerBot, question: str) -> str:
        try:
            return answerer.respond(question)
        except Exception as e:
            print("OOPS SOMETHING WENT WRONG!")
            self.scores[answerer] -= EXCEPTION_PENALTY
            return None

    def handle_validation_result(self, guesser: PlayerBot, validation_result: ValidationResult):
        if validation_result is ValidationResult.INVALID:
            print("INVALID QUESTION")
            self.scores[guesser] -= INVALID_QUESTION_PENALTY
        elif validation_result is ValidationResult.CHARACTER_GUESSED:
            print("CHARACTER GUESSED")
        elif validation_result is ValidationResult.CHARACTER_NOT_GUESSED:
            print("WRONG GUESS")
            self.scores[guesser] -= CHARACTER_NOT_GUESSED_PENALTY

    def set_character_for_referees(self, character: str):
        for ref in self.referees:
            ref.set_character(character)

    def reset_scores(self):
        self.scores = {self.bot1: INITIAL_SCORE, self.bot2: INITIAL_SCORE}

    def print_scores(self):
        print("RESULTS")
        print(self.bot1.name + ": " + str(self.scores[self.bot1]))
        print(self.bot2.name + ": " + str(self.scores[self.bot2]))

    def get_winner(self) -> PlayerBot:
        winner = self.bot1 if self.scores[self.bot1] > self.scores[self.bot2] else self.bot2
        print("THE WINNER IS: " + winner.name)
        return winner

    def get_looser(self) -> PlayerBot:
        looser = self.bot1 if self.scores[self.bot1] < self.scores[self.bot2] else self.bot2
        return looser

    def validate_question(self, question: str,) -> ValidationResult:
        results = []
        for ref in self.referees:
            results.append(ref.validate_question(question))
        return max(set(results), key=results.count)

    def validate_answer(self, question: str, answer: str) -> ValidationResult:
        results = []
        for ref in self.referees:
            results.append(ref.validate_answer(question, answer))
        return max(set(results), key=results.count)
