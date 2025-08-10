from dataclasses import dataclass, field
from typing import Set, List, Optional


# Визначення класу Teacher
@dataclass
class Teacher:
    first_name: str
    last_name: str
    age: int
    email: str
    can_teach_subjects: Set[str]
    assigned_subjects: Set[str] = field(default_factory=set)

def create_schedule(subjects: Set[str], teachers: List[Teacher]) -> Optional[List[Teacher]]:
    uncovered = set(subjects)
    selected: List[Teacher] = []
    used = set()

    while uncovered:
        best_idx = None
        best_covers = set()

        for i, t in enumerate(teachers):
            if i in used:
                continue
            covers = t.can_teach_subjects & uncovered
            if not best_idx or len(covers) > len(best_covers):
                best_idx, best_covers = i, covers
            elif len(covers) == len(best_covers) and len(covers) > 0:
                if teachers[i].age < teachers[best_idx].age:
                    best_idx, best_covers = i, covers

        if not best_idx and len(best_covers) == 0:
            return None
        if best_idx is None or len(best_covers) == 0:
            return None

        chosen = teachers[best_idx]
        chosen.assigned_subjects = set(best_covers)
        selected.append(chosen)
        used.add(best_idx)
        uncovered -= best_covers

    selected.sort(key=lambda t: (t.last_name, t.first_name))
    return selected

if __name__ == '__main__':
    # Множина предметів
    subjects = {'Математика', 'Фізика', 'Хімія', 'Інформатика', 'Біологія'}

    # Створення списку викладачів
    teachers = [
        Teacher("Олександр", "Іваненко", 45, "o.ivanenko@example.com", {"Математика", "Фізика"}),
        Teacher("Марія", "Петренко", 38, "m.petrenko@example.com", {"Хімія"}),
        Teacher("Сергій", "Коваленко", 50, "s.kovalenko@example.com", {"Інформатика", "Математика"}),
        Teacher("Наталія", "Шевченко", 29, "n.shevchenko@example.com", {"Біологія", "Хімія"}),
        Teacher("Дмитро", "Бондаренко", 35, "d.bondarenko@example.com", {"Фізика", "Інформатика"}),
        Teacher("Олена", "Гриценко", 42, "o.grytsenko@example.com", {"Біологія"}),
    ]

    # Виклик функції створення розкладу
    schedule = create_schedule(subjects, teachers)

    # Виведення розкладу
    if schedule is None:
        print("Неможливо покрити всі предмети наявними викладачами.")
    else:
        print("Розклад занять:")
        for t in schedule:
            subj_list = ", ".join(sorted(t.assigned_subjects))
            print(f"{t.first_name} {t.last_name}, {t.age} років, email: {t.email}")
            print(f"   Викладає предмети: {subj_list}\n")
