from time import sleep

from colorama import Fore, Style

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
        print(Fore.BLUE + "GAME STARTING " + self.bot1.name + " VS " + self.bot2.name)
        print(Style.RESET_ALL)
        while self.scores[self.bot1] == self.scores[self.bot2]:
            self.reset_scores()
            self.play_rounds()
            if self.scores[self.bot1] == self.scores[self.bot2]:
                print(Fore.BLUE + "TIE BREAKER")
        print(Style.RESET_ALL)

        return self.get_winner()

    def play_rounds(self):
        self.play_round(self.bot1, self.bot2)
        print(Fore.BLUE + "SWITCHING SIDES")
        print(Style.RESET_ALL)
        self.play_round(self.bot2, self.bot1)
        self.print_scores()

    def play_round(self, answerer: PlayerBot, guesser: PlayerBot):
        secret_character = answerer.choose_character()
        print(Fore.GREEN + answerer.name + " has selected the secret character:\n" + secret_character)
        print(Style.RESET_ALL)
        self.set_character_for_referees(secret_character)
        response = None

        while self.scores[guesser] > 0:
            sleep(2)
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
            self.scores[guesser] -= 1

    def ask_question(self, guesser: PlayerBot, response: str) -> str|None:
        try:
            return guesser.ask_question(response)
        except Exception as e:
            print(Fore.RED + "OOPS SOMETHING WENT WRONG!")
            print(Style.RESET_ALL)
            self.scores[guesser] -= EXCEPTION_PENALTY
            return None

    def get_answer(self, answerer: PlayerBot, question: str) -> str|None:
        try:
            return answerer.respond(question)
        except Exception as e:
            print(Fore.RED + "OOPS SOMETHING WENT WRONG!")
            print(Style.RESET_ALL)
            self.scores[answerer] -= EXCEPTION_PENALTY
            return None

    def handle_validation_result(self, guesser: PlayerBot, validation_result: ValidationResult):
        if validation_result is ValidationResult.INVALID:
            print(Fore.RED + "INVALID QUESTION")
            print(Style.RESET_ALL)
            self.scores[guesser] -= INVALID_QUESTION_PENALTY
        elif validation_result is ValidationResult.CHARACTER_GUESSED:
            print(Fore.GREEN + "CHARACTER GUESSED")
            print(Style.RESET_ALL)
        elif validation_result is ValidationResult.CHARACTER_NOT_GUESSED:
            print(Fore.RED + "WRONG GUESS")
            print(Style.RESET_ALL)
            self.scores[guesser] -= CHARACTER_NOT_GUESSED_PENALTY

    def set_character_for_referees(self, character: str):
        for ref in self.referees:
            ref.set_character(character)

    def reset_scores(self):
        self.scores = {self.bot1: INITIAL_SCORE, self.bot2: INITIAL_SCORE}

    def print_scores(self):
        print(Fore.BLUE + "RESULTS")
        print(self.bot1.name + ": " + str(self.scores[self.bot1]))
        print(self.bot2.name + ": " + str(self.scores[self.bot2]))
        print(Style.RESET_ALL)

    def get_winner(self) -> PlayerBot:
        winner = self.bot1 if self.scores[self.bot1] > self.scores[self.bot2] else self.bot2
        print(Fore.BLUE + "THE WINNER IS: " + winner.name)
        print(Style.RESET_ALL)
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
