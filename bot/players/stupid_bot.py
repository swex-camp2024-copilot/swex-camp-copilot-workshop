import random

from bot.player import PlayerBot

characters = ["Alber Einstein", "Isaac Newton", "Bill Gates", "Steve Jobs",
              "Elon Musk", "Mark Zuckerberg", "Jeff Bezos", "Warren Buffet",
              "Oprah Winfrey", "Ellen DeGeneres", "Taylor Swift", "Beyonce",
              "Rihanna", "Katy Perry", "Lady Gaga", "Adele", "Justin Bieber",
              "Ed Sheeran", "Drake", "Kendrick Lamar", "Jay-Z", "Kanye West",
              "Eminem", "Snoop Dogg", "50 Cent", "Lil Wayne", "Nicki Minaj",
              "Cardi B", "Megan Thee Stallion", "Doja Cat", "Ariana Grande",
              "Selena Gomez", "Demi Lovato", "Miley Cyrus", "Shawn Mendes",
              "Harry Styles", "Zayn Malik", "Niall Horan", "Louis Tomlinson",
              "Liam Payne", "Zac Efron", "Robert Pattinson", "Tom Holland",
              "Chris Hemsworth", "Chris Evans", "Chris Pratt", "Chris Pine",
              "Chris Rock", "Chris Tucker", "Chris Brown", "Chris Martin",
              "Chris Stapleton", "Chris Young", "Chris Stapleton",
              "Chris Young", "Chris Lane", "Chris Janson", "Chris Daughtry",
              "Chris Kirkpatrick", "Chris O'Donnell", "Chris Noth",
              "Chris Kattan", "Chris Elliott"]


class StupidPlayerBot(PlayerBot):
    def __init__(self):
        super().__init__("Stupid Bot")
        self.character = ""

    def choose_character(self) -> str:
        # returns random character from the list of characters
        self.character = random.choice(characters)
        return self.character

    def ask_question(self, query: str) -> str:
        guess = random.choice(characters)
        return "Is your character " + guess + "?"

    def respond(self, query: str) -> str:
        # check if the query contains the character's name
        if self.character in query:
            return "Yes"
        else:
            return "No"
