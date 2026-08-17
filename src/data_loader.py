from models.examiners import Examiner
from models.student import Student

import sys

def get_examiners():
    examiners = []
    try:
        with open('data/examiners.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = line.split()
                if len(parts) < 2: continue
                examiner = Examiner(parts[0], parts[1])
                examiners.append(examiner)
    except FileNotFoundError:
        print("Ошибка: файл examiners.txt не найден")
        sys.exit(1)
    return examiners

def get_students():
    students = []
    try:
        with open('data/students.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                parts = line.split()
                if len(parts) < 2: continue
                student = Student(parts[0], parts[1])
                students.append(student)
    except FileNotFoundError:
        print("Ошибка: файл students.txt не найден")
        sys.exit(1)
    return students

def get_questions():
    questions = []
    try:
        with open('data/questions.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    questions.append(line)
    except:
        print("Ошибка: файл questions.txt не найден")
        sys.exit(1)
    return questions
