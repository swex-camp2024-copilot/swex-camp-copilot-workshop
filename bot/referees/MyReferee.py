from bot.referee import RefereeBot, ValidationResult

class MyReferee(RefereeBot):
    def __init__(self):
        super().__init__("MyReferee")

    def set_character(self, name):
        self.character = name

    def validate_question(self, question: str) -> ValidationResult:
        if self.character in question:
            return ValidationResult.CHARACTER_GUESSED
        return ValidationResult.CHARACTER_NOT_GUESSED
    
    def validate_answer(self, question: str, answer: str) -> ValidationResult:
        if self.character in answer:
            return ValidationResult.CHARACTER_GUESSED
        return ValidationResult.CHARACTER_NOT_GUESSED
    
    def reset(self):
        pass