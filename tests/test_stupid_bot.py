import unittest
import random
from bot.players.stupid_bot import StupidPlayerBot, characters

class TestStupidPlayerBot(unittest.TestCase):

  def setUp(self):
    self.bot = StupidPlayerBot()

  def test_choose_character(self):
    character = self.bot.choose_character()
    self.assertIn(character, characters)
    self.assertEqual(character, self.bot.character)

  def test_ask_question(self):
    question = self.bot.ask_question("query")
    self.assertTrue(question.startswith("Is your character "))
    self.assertTrue(question.endswith("?"))

  def test_respond(self):
    self.bot.character = "test_character"
    self.assertEqual(self.bot.respond("Is your character test_character?"), "Yes")
    self.assertEqual(self.bot.respond("Is your character other_character?"), "No")

  def test_reset(self):
    self.bot.character = "test_character"
    self.bot.reset()
    self.assertEqual(self.bot.character, "")

if __name__ == "__main__":
  unittest.main()