import random
from time import sleep

from bot.player import PlayerBot
from game.game import Game


class Tournament:
    def __init__(self, players, referees):
        self.players = players
        self.referees = referees

    def play(self) -> PlayerBot:
        while len(self.players) > 1:
            winners = []
            for i in range(0, len(self.players), 2):
                if i + 1 < len(self.players):
                    game = Game(self.players[i], self.players[i + 1], self.referees)
                    winner = game.play()
                    winners.append(winner)
                    sleep(2)
                else:
                    # If there is an odd number of players, the last player advances to the next round
                    winners.append(self.players[i])
            random.shuffle(winners)
            self.players = winners
            print("ROUND FINISHED")
            if len(winners) > 1:
                print("THE WINNERS ARE:")
                for winner in winners:
                    print(winner.name)
            # press any key to continue
            print("Press any key to continue")
            input()

        print(f"THE WINNER OF THE TOURNAMENT IS {self.players[0].name}")
        return self.players[0]