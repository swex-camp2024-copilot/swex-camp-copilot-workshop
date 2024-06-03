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
        while self.scores[self.bot1] == self.scores[self.bot2]:
            self.scores = {self.bot1: INITIAL_SCORE, self.bot2: INITIAL_SCORE}
            self.play_round(self.bot1, self.bot2)
            self.play_round(self.bot2, self.bot1)
            if self.scores[self.bot1] == self.scores[self.bot2]:
                print("TIE BREAKER")

        print("RESULTS")
        print(self.bot1.name + ": " + str(self.scores[self.bot1]))
        print(self.bot2.name + ": " + str(self.scores[self.bot2]))
        winner = self.bot1 if self.scores[self.bot1] > self.scores[self.bot2] else self.bot2
        print("THE WINNER IS: " + winner.name)
        return winner

    def play_round(self, answerer: PlayerBot, guesser: PlayerBot):
        secret_character = answerer.choose_character()
        print(answerer.name + " has chosen " + secret_character)
        # set the character for the referees
        for ref in self.referees:
            ref.set_character(secret_character)
        response = None

        while self.scores[guesser] > 0:
            sleep(2)
            self.scores[guesser] -= 1

            question = ""
            try:
                question = guesser.ask_question(response)
            except Exception as e:
                print("OOPS SOMETHING WENT WRONG!")
                self.scores[guesser] -= EXCEPTION_PENALTY
                continue

            print(guesser.name + ": " + question)

            validation_result = self.validate_question(question)
            if validation_result is ValidationResult.INVALID:
                print("INVALID QUESTION")
                self.scores[guesser] -= INVALID_QUESTION_PENALTY
                break
            if validation_result is ValidationResult.CHARACTER_GUESSED:
                print("CHARACTER GUESSED")
                break
            if validation_result is ValidationResult.CHARACTER_NOT_GUESSED:
                print("WRONG GUESS")
                self.scores[guesser] -= CHARACTER_NOT_GUESSED_PENALTY
                break

            response = answerer.respond(question)
            print(answerer.name + ": " + response)
            if self.validate_answer(question, response) is ValidationResult.INVALID:
                self.scores[answerer] -= DISQUALIFICATION_PENALTY
                break

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
