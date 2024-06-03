import random

from bot.player import PlayerBot
from game.game import Game


class Tournament:
    def __init__(self, players, referees):
        self.players = players
        self.referees = referees

    def play(self) -> PlayerBot:
        while len(self.players) > 1:
            winners = []
            loosers = []
            for i in range(0, len(self.players), 2):
                if i + 1 < len(self.players):
                    game = Game(self.players[i], self.players[i + 1], self.referees)
                    winner = game.play()
                    winners.append(winner)
                    loosers.append(game.get_looser())
                    print("Game finished. Press any key to continue.")
                    input()
                else:
                    lucky_looser = random.choice(loosers)
                    print("Lucky looser is " + lucky_looser.name)
                    game = Game(self.players[i], lucky_looser, self.referees)
                    winner = game.play()
                    winners.append(winner)
                    print("Game finished. Press any key to continue.")
                    input()
            random.shuffle(winners)
            self.players = winners
            if len(winners) > 1:
                print("ROUND FINISHED")
                print("THE WINNERS ARE:")
                for player in self.players:
                    player.reset()
                    print(player.name)
                print("Press any key to continue")
                input()

        print(f"THE WINNER OF THE TOURNAMENT IS {self.players[0].name}")
        return self.players[0]