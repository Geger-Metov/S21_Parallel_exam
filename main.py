from data_loader import get_examiners, get_questions, get_students
from simulation import monitor, worker

import multiprocessing as mp
import time


def main():
    examiners = get_examiners()
    students = get_students()
    questions = get_questions()

    total_students = len(students)

    update_queue = mp.Queue()
    students_queue = mp.Queue()
    for  i in students:
        students_queue.put(i)

    manager = mp.Manager()
    students_state = manager.dict()
    questions_stat = manager.dict()

    global_start = time.time()
    stop_event = mp.Event()
    processes = []
    for ex in examiners:
        p = mp.Process(target=worker, args=(ex, students_queue, questions, 
                                            update_queue, students_state, 
                                            questions_stat, global_start, stop_event))
        processes.append(p)
        p.start()
    
    monitor(examiners, students, update_queue, students_state, questions_stat,
        total_students, global_start, processes)

    stop_event.set()
    for p in processes:
        p.join(timeout=1)


if __name__ == '__main__':
    mp.freeze_support()
    main()
