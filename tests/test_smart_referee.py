import unittest
from unittest.mock import patch
from bot.referees.smart_referee import SmartReferee

class TestSmartReferee(unittest.TestCase):
  def test_validate_question1(self):
    referee = SmartReferee()
    result = referee.validate_question("Are you an actor?")
    self.assertEqual(result, "VALID")

  def test_validate_question2(self):
    referee = SmartReferee()
    result = referee.validate_question("Tell me who you are?")
    self.assertEqual(result, "INVALID")

  def test_validate_question_character_guess(self):
    referee = SmartReferee()
    referee.set_character("Sherlock Holmes")
    result = referee.validate_question("Are you Sherlock Holmes?")
    self.assertEqual(result, "CHARACTER_GUESSED")

  def test_validate_answer(self):
    referee = SmartReferee()
    referee.set_character("Sherlock Holmes")
    result = referee.validate_answer("Are you a detective?", "yes")
    self.assertEqual(result, "VALID")

if __name__ == '__main__':
  unittest.main()