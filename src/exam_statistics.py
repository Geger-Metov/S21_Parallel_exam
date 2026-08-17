def get_best_students(students, students_state):
    passed_with_time = []
    for s in students:
        if s.name in students_state and students_state[s.name]['status'] == 'passed':
            t = students_state[s.name].get('exam_end_time')
            if t is not None:
                passed_with_time.append((s.name, t))
    if not passed_with_time:
        return []
    min_t = min(t for _, t in passed_with_time)
    return [name for name, t in passed_with_time if t == min_t]

def get_best_examiners(examiners):
    rates = []
    for ex in examiners:
        total = ex.total_students
        failed = ex.failed_students
        percent = failed / total if total > 0 else 1.0
        rates.append((ex.name, percent))
    if not rates:
        return []
    min_p = min(p for _, p in rates)
    return [name for name, p in rates if p == min_p]

def get_expelled_students(students, students_state):
    failed_with_time = []
    for s in students:
        if s.name in students_state and students_state[s.name]['status'] == 'failed':
            t = students_state[s.name].get('exam_end_time')
            if t is not None:
                failed_with_time.append((s.name, t))
    if not failed_with_time:
        return []
    min_fail = min(t for _, t in failed_with_time)
    return [name for name, t in failed_with_time if t == min_fail]

def get_best_questions(questions_stats):
    if not questions_stats:
        return []
    max_correct = max(questions_stats.values())
    return [q for q, cnt in questions_stats.items() if cnt == max_correct]
