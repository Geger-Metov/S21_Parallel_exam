from utils import golden_ratio

class Student():
    def __init__(self, name : str, gender : str):
        self.name = name
        self.gender = gender
        self.status = "queue"

    def answer_a_question(self, question : str) -> str:
        words = question.split()
        return golden_ratio(self.gender, words)
        