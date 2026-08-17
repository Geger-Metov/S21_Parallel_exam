from exam_statistics import get_best_students, get_best_examiners, get_expelled_students, get_best_questions

import prettytable
import os
import time

def draw_students_table(students, students_state, final=False):
    rows = []
    for s in students:
        if s.name in students_state:
            status = "Сдал" if students_state[s.name]["status"] == "passed" else "Провалил"
        else:
            if final:
                continue
            status = "Очередь"
        rows.append([s.name, status])

    if not final:
        def status_order(status):
            return 0 if status == "Очередь" else (1 if status == "Сдал" else 2)
    
        rows.sort(key= lambda x: status_order(x[1]))
    else:
        rows.sort(key=lambda x: 0 if x[1] == "Сдал" else 1)

    table = prettytable.PrettyTable()
    table.field_names = ["Студент", "Статус"]
    for i in rows:
        table.add_row(i)
    return table

def draw_examiners_table(examiners, final=False):
    table = prettytable.PrettyTable()
    if not final:
        table.field_names = ["Экзаменатор", "Текущий студент", "Всего студентов", 
                             "Завалил", "Время работы"]
        for ex in examiners:
            current = ex.current_student if ex.current_student is not None else '-'
            table.add_row([ex.name, current, ex.total_students, ex.failed_students, 
                           f"{ex.working_time:.2f}"])
    else:
        table.field_names = ["Экзаменатор", "Всего студентов", "Завалил", "Время работы"]
        for ex in examiners:
            table.add_row([ex.name, ex.total_students, ex.failed_students, 
                           f"{ex.working_time:.2f}"])

    return table

def print_final_stats(examiners, students, students_state, questions_stats, total_students, global_start):
    clear_screen()

    final_stud_table = draw_students_table(students, students_state, final=True)
    print(final_stud_table, end='\n\n')
    final_exam_table = draw_examiners_table(examiners, final=True)
    print(final_exam_table, end='\n\n')

    total_time = time.time() - global_start
    print(f"Время с момента начала экзамена и до момента и его завершения: {total_time:.2f}")

    best_students = get_best_students(students, students_state)
    print(f"Имена лучших студентов: {', '.join(best_students) if best_students else 'нет'}")

    best_examiners = get_best_examiners(examiners)
    print(f"Имена лучших экзаменаторов: {', '.join(best_examiners) if best_examiners else 'нет'}")

    expelled = get_expelled_students(students, students_state)
    print(f"Имена студентов, которых после экзамена отчислят: {', '.join(expelled) if expelled else 'нет'}")

    best_questions = get_best_questions(questions_stats)
    print(f"Лучшие вопросы: {', '.join(best_questions) if best_questions else 'нет'}")

    total_passed = sum(1 for s in students if s.name in students_state and students_state[s.name]['status'] == 'passed')
    print("Вывод: экзамен удался" if total_passed > 0.85 * total_students else "Вывод: экзамен не удался")

def clear_screen():
    os.system("clear" if os.name == "posix" else "cls")
