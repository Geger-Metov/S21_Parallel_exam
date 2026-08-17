from utils import golden_ratio
from config import BAD_MOOD_PROB, GOOD_MOOD_PROB, CONTINUE_ANSWER_PROB, LUNCH_DURATION_MAX, LUNCH_DURATION_MIN

from random import uniform, choice, random


class Examiner():
    def __init__(self, name : str, gender : str):
        self.name = name
        self.gender = gender
        self.total_students = 0
        self.failed_students = 0
        self.working_time = 0.0
        self.current_student = None
        self.on_lunch = False
    
    def lunch(self) -> float:
        return uniform(LUNCH_DURATION_MIN, LUNCH_DURATION_MAX)

    def exam_duration(self) -> float:
        duration = len(self.name)
        return uniform(duration - 1, duration + 1)

    def ask_question(self, questions_bank: list[str]) -> str:
        return choice(questions_bank)

    def think_about_answer(self, question : str) -> set:
        words = question.split()
        answers = set()
        answer = golden_ratio(self.gender, words)
        answers.add(answer)
        words.remove(answer)

        while words and random() < CONTINUE_ANSWER_PROB:
            answer = golden_ratio(self.gender, words)
            answers.add(answer)
            words.remove(answer)
        
        return answers

    def give_a_rating(self, correct_answer_cnt : int, wrong_answer_cnt : int) -> bool:
        mood = random()
        if mood < BAD_MOOD_PROB:
            return False
        elif mood < BAD_MOOD_PROB + GOOD_MOOD_PROB:
            return True
        return correct_answer_cnt > wrong_answer_cnt
