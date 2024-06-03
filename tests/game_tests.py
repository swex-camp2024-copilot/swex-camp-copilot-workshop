import unittest
from unittest.mock import Mock
from bot.referee import ValidationResult
from game.game import Game, INITIAL_SCORE, INVALID_QUESTION_PENALTY, CHARACTER_NOT_GUESSED_PENALTY, DISQUALIFICATION_PENALTY


class TestGame(unittest.TestCase):
    def setUp(self):
        self.bot1 = Mock()
        self.bot2 = Mock()
        self.referee = Mock()
        self.game = Game(self.bot1, self.bot2, [self.referee])

    def test_play_round_with_invalid_question(self):
        self.bot1.choose_character.return_value = 'character'
        self.bot2.ask_question.return_value = 'question'
        self.referee.validate_question.return_value = ValidationResult.INVALID

        self.game.play_round(self.bot1, self.bot2)

        self.assertEqual(self.game.scores[self.bot2], INITIAL_SCORE - INVALID_QUESTION_PENALTY - 1)

    def test_play_round_with_character_guessed(self):
        self.bot1.choose_character.return_value = 'character'
        self.bot2.ask_question.return_value = 'question'
        self.referee.validate_question.return_value = ValidationResult.CHARACTER_GUESSED

        self.game.play_round(self.bot1, self.bot2)

        self.assertEqual(self.game.scores[self.bot2], INITIAL_SCORE - 1)

    def test_play_round_with_character_not_guessed(self):
        self.bot1.choose_character.return_value = 'character'
        self.bot2.ask_question.return_value = 'question'
        self.referee.validate_question.return_value = ValidationResult.CHARACTER_NOT_GUESSED

        self.game.play_round(self.bot1, self.bot2)

        self.assertEqual(self.game.scores[self.bot2], INITIAL_SCORE - CHARACTER_NOT_GUESSED_PENALTY - 1)

    def test_play_round_with_invalid_answer(self):
        self.bot1.choose_character.return_value = 'character'
        self.bot2.ask_question.return_value = 'question'
        self.bot1.respond.return_value = 'answer'
        self.referee.validate_question.return_value = ValidationResult.VALID
        self.referee.validate_answer.return_value = ValidationResult.INVALID

        self.game.play_round(self.bot1, self.bot2)

        self.assertEqual(self.game.scores[self.bot1], INITIAL_SCORE - DISQUALIFICATION_PENALTY)

    def test_play_with_bot1_winning(self):
        self.bot1.choose_character.return_value = 'character'
        self.bot2.ask_question.return_value = 'question'
        self.bot1.respond.return_value = 'answer'
        self.referee.validate_question.return_value = ValidationResult.VALID
        self.referee.validate_answer.return_value = ValidationResult.VALID
        self.game.scores[self.bot1] = 10
        self.game.scores[self.bot2] = 5

        winner = self.game.play()

        self.assertEqual(winner, self.bot1)

    def test_play_with_bot2_winning(self):
        self.bot1.choose_character.return_value = 'character'
        self.bot2.ask_question.return_value = 'question'
        self.bot1.respond.return_value = 'answer'
        self.referee.validate_question.return_value = ValidationResult.VALID
        self.referee.validate_answer.return_value = ValidationResult.VALID
        self.game.scores[self.bot1] = 5
        self.game.scores[self.bot2] = 10

        winner = self.game.play()

        self.assertEqual(winner, self.bot2)

    # test validate_question method with multiple referees
    # where all but one referee returns VALID
    def test_validate_question_with_multiple_referees(self):
        self.referee1 = Mock()
        self.referee2 = Mock()
        self.game = Game(self.bot1, self.bot2, [self.referee, self.referee1, self.referee2])
        self.referee.validate_question.return_value = ValidationResult.VALID
        self.referee1.validate_question.return_value = ValidationResult.VALID
        self.referee2.validate_question.return_value = ValidationResult.INVALID

        result = self.game.validate_question('question')

        self.assertEqual(result, ValidationResult.VALID)


if __name__ == '__main__':
    unittest.main()