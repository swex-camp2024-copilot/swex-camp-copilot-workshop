from pkgutil import walk_packages

from game.tournament import Tournament


def load(package, condition):
    bots = []
    for importer, modname, ispkg in walk_packages(package):
        module = importer.find_module(modname).load_module(modname)
        for name in dir(module):
            obj = getattr(module, name)
            if hasattr(obj, "__bases__") and condition(obj):
                bots.append(obj())
    return bots


def main():
    players = load(["bot/players"], lambda x: x.__bases__[0].__name__ == "PlayerBot")
    referees = load(["bot/referees"], lambda x: x.__bases__[0].__name__ == "RefereeBot")

    if len(players) == 0:
        print("No players found")
        return

    if len(referees) == 0:
        print("No referees found")
        return

    tournament = Tournament(players, referees)
    tournament.play()


if __name__ == "__main__":
    main()
