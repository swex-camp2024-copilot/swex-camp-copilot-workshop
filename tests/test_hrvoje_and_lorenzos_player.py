from bot.players.hrvoje_and_lorenzos_unbeatable_player import HrvojeAndLorenzosUnbeatablePlayer


def test_choose_character_generates_valid_response():
    player = HrvojeAndLorenzosUnbeatablePlayer()
    character = player.choose_character()
    assert isinstance(character, str) and len(character) > 0


def test_respond_generates_valid_response():
    player = HrvojeAndLorenzosUnbeatablePlayer()
    player.character = "Roman Josi"
    response_is_a_hockey_player_yes = player.respond("Is your character a hockey player?")
    response_is_a_woman_no = player.respond("Is your character a woman?")
    response_correct_character_yes = player.respond("Is your character Roman Josi?")
    response_wrong_character_no = player.respond("Is your character Taylor Swift?")

    assert "yes" in response_is_a_hockey_player_yes.lower()
    assert "no" in response_is_a_woman_no.lower()
    assert "yes" in response_correct_character_yes.lower()
    assert "no" in response_wrong_character_no.lower()


def test_ask_question_generates_valid_response():
    player_asker = HrvojeAndLorenzosUnbeatablePlayer()
    player_answerer = HrvojeAndLorenzosUnbeatablePlayer()
    player_answerer.character = "Lionel Messi"
    question = ""
    response = ""
    counter = 0

    while "lionel messi" not in question.lower():
        question = player_asker.ask_question(response)
        response = player_answerer.respond(question)
        assert counter < 50, "The loop is running too long. Check the code."
        counter += 1
