class Puzzle:
    #initialize
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def check_answer(self, player_answer):
        return player_answer.strip().lower() == self.answer.lower()