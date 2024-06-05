# GUESS THE SECRET PERSON

Bunch of bots imagining a person and guessing who is the person other bots imagined.
Some bots are not imagining and guessing, they are referees.

## Game Rules

- Each round is played by 2 bots and includes referees.
- One bot is the guesser and the other is the answerer.
- The guesser asks questions to the answerer to guess the secret person.
- The question must be a yes/no question.
- The answerer can only answer with "yes" or "no". They are allowed to provide more information (although that wouldn't be smart) but they cannot lie!
- The guesser can guess the secret person at any time. When the bot makes their guess the game is finished and points are calculated as defined in game.py.
- Each question and answer are evaluated by the referees.
- Each round consists of at least 2 games. In each game, the guesser and the answerer roles are switched.
- The bot with the most points at the end of the round wins.


## Installation
```bash
pip install python-dotnet
pip install colorama
```

## Player bot creation

- Create a new python file in the `bot\players` directory.
- Bot must extend the `PlayerBot` class.
- __init__ method must take only the self parameter
- implement all abstract methods

## Player bot creation

- Create a new python file in the `bot\referees` directory.
- Bot must extend the `RefereeBot` class.
- __init__ method must take only the self parameter
- implement all abstract methods

## Environment Variables

- Store all API Keys and other sensitive information in a `.env` file in the root directory
- If you are not using provided API keys then name your environment variable to include your team name (e.g. `TEAM_NAME_GROQ_API_KEY`)
- If you're using provided OpenAI API Key, name the environment variable `OPENAI_API_KEY` 
- use os.getenv to get the value of the environment variable