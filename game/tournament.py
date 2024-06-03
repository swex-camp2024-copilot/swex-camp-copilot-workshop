from bot.player import PlayerBot
from bot.referee import ValidationResult


def play(players, referees) -> PlayerBot:
    while True:
        if len(players) < 2:
            print("No players found.")
            break
        if len(referees) == 0:
            print("No referees found.")
            break

        while len(players) > 1:
            winners = []
            for i in range(0, len(players), 2):
                if i + 1 < len(players):
                    # score for the player[i]
                    player1_score = 25
                    # score for the player[i+1]
                    player2_score = 25

                    # Play a game with two players
                    answerer = players[i]
                    guesser = players[i + 1]
                    referee = referees[0]

                    player1_character = answerer.choose_character()
                    referee.set_character(player1_character)
                    response = None

                    while player2_score > 0:
                        player2_score -= 1
                        if response:
                            question = guesser.ask_question(response)
                        else:
                            question = guesser.initial_question()

                        if referee.validate_question(question) is ValidationResult.INVALID:
                            player2_score -= 50
                            break
                        if referee.validate_question(question) is ValidationResult.CHARACTER_GUESSED:
                            break
                        if referee.validate_question(question) is ValidationResult.CHARACTER_NOT_GUESSED:
                            player2_score -= 25
                            break

                        response = answerer.respond(question)
                        if referee.validate_question(question) is ValidationResult.INVALID:
                            # answerer is disqualified
                            player1_score -= 1000
                            break

                    guesser = players[i]
                    answerer = players[i + 1]
                    while player1_score > 0:
                        player1_score -= 1
                        if response:
                            question = guesser.ask_question(response)
                        else:
                            question = guesser.initial_question()

                        if referee.validate_question(question) is ValidationResult.INVALID:
                            player1_score -= 50
                            break
                        if referee.validate_question(question) is ValidationResult.CHARACTER_GUESSED:
                            break
                        if referee.validate_question(question) is ValidationResult.CHARACTER_NOT_GUESSED:
                            player1_score -= 25
                            break

                        response = answerer.respond(question)
                        if referee.validate_question(question) is ValidationResult.INVALID:
                            # answerer is disqualified
                            player2_score -= 1000
                            break
                    if player1_score > player2_score:
                        winners.append(players[i])
                    else:
                        winners.append(players[i + 1])
                else:
                    # If there is an odd number of players, the last player advances to the next round
                    winners.append(players[i])
            players = winners

        # The last player is the winner of the tournament
        print(f"The winner of the tournament is {players[0].name}")
        return players[0]