from display import clear_screen, draw_examiners_table, draw_students_table, print_final_stats
from config import QUESTIONS_PER_STUDENT, LUNCH_START_TIME

import time
from queue import Empty

def worker(examiner, student_queue, questions_bank, update_queue, 
           students_state, questions_stat, global_start, stop_event):
    total = 0
    failed = 0
    work_time = 0.0
    on_lunch = False
    has_taken_lunch = False

    def send_updates(**kwargs):
        update_queue.put((examiner.name, kwargs))

    while not stop_event.is_set():
        if on_lunch:
            send_updates(current_student=None, on_lunch=True)
            time.sleep(examiner.lunch())
            on_lunch = False
            send_updates(on_lunch=False)
            continue

        if not has_taken_lunch and (time.time() - global_start) >= LUNCH_START_TIME:
            on_lunch = True
            has_taken_lunch = True
            continue

        try:
            student = student_queue.get_nowait()
        except Empty:
            break
        
        total += 1
        send_updates(current_student=student.name, total_students=total)

        correct = 0
        wrong = 0
        for _ in range(QUESTIONS_PER_STUDENT):
            question = examiner.ask_question(questions_bank)
            student_answer = student.answer_a_question(question)
            correct_set = examiner.think_about_answer(question)
            if student_answer in correct_set:
                correct += 1
                questions_stat[question] = questions_stat.get(question, 0) + 1
            else:
                wrong += 1

        passed = examiner.give_a_rating(correct, wrong)
        if not passed:
            failed += 1
            send_updates(failed=failed)
            status = "failed"
        else:
            status = "passed"
        
        duration = examiner.exam_duration()
        time.sleep(duration)
        work_time += duration
        send_updates(work_time=work_time)

        students_state[student.name] = {
            "status": status,
            "exam_end_time": time.time()
        }
        send_updates(current_student=None)
    
    send_updates(current_student=None)

def monitor(examiners, students, update_queue, students_state, questions_stat,
            total_students, global_start, processes):
    # Создаём словарь для быстрого доступа к экзаменаторам по имени
    examiners_dict = {ex.name: ex for ex in examiners}

    while any(p.is_alive() for p in processes):
        while True:
            try:
                name, updates = update_queue.get_nowait()
                ex = examiners_dict[name]
                if 'current_student' in updates:
                    ex.current_student = updates['current_student']
                if 'total_students' in updates:
                    ex.total_students = updates['total_students']
                if 'failed' in updates:
                    ex.failed_students = updates['failed']
                if 'work_time' in updates:
                    ex.working_time = updates['work_time']
                if 'on_lunch' in updates:
                    ex.on_lunch = updates['on_lunch']
            except Empty:
                break

        clear_screen()
        print(draw_students_table(students, students_state), end='\n\n')
        print(draw_examiners_table(examiners), end='\n\n')
        remaining = sum(1 for s in students if s.name not in students_state)
        print(f"Осталось в очереди: {remaining} из {total_students}")
        print(f"Время с момента начала экзамена: {time.time() - global_start:.2f}")
        time.sleep(0.2)
    
    print_final_stats(examiners, students, students_state, questions_stat, total_students, global_start)
        