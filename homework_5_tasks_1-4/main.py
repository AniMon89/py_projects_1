class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer_hw(self, lecturer, course, lecture_s_grade):
        if isinstance(lecturer,Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress and lecture_s_grade in range(1,11):
            if course in lecturer.grades:
                lecturer.grades[course] += [lecture_s_grade]
            else:
                lecturer.grades[course] = [lecture_s_grade]
        else:
            return 'Ошибка'

    def find_mean_of_grades_student(self):
        if not self.grades:
            return 0
        list_grades_student = []
        for el in self.grades.values():
            list_grades_student.extend(el)
        return round(sum(list_grades_student)/len(list_grades_student),1)

    def __str__(self):
        return f"""Имя: {self.name}
        \rФамилия: {self.surname}
        \rСредняя оценка за домашние задания: {self.find_mean_of_grades_student()}
        \rКурсы в процессе изучения: {', '.join(self.courses_in_progress)}
        \rЗавершенные курсы: {', '.join(self.finished_courses)}\n"""

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception('Объект не принадлежит этому классу.')
        return self.find_mean_of_grades_student() < other.find_mean_of_grades_student()

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception('Объект не принадлежит этому классу.')
        return self.find_mean_of_grades_student() <= other.find_mean_of_grades_student()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception('Объект не принадлежит этому классу.')
        return self.find_mean_of_grades_student() == other.find_mean_of_grades_student()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []
        self.grades = {}

    def find_mean_of_grades_lecturer(self):
        if not self.grades:
            return 0
        list_grades_lecturer = []
        for el_ in self.grades.values():
            list_grades_lecturer.extend(el_)
        return round(sum(list_grades_lecturer)/len(list_grades_lecturer),1)

    def __str__(self):
        return f"""Имя: {self.name}
                \rФамилия: {self.surname}
                \rСредняя оценка за лекции: {self.find_mean_of_grades_lecturer()}\n"""

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception('Объект не принадлежит этому классу.')
        return self.find_mean_of_grades_lecturer() < other.find_mean_of_grades_lecturer()

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception('Объект не принадлежит этому классу.')
        return self.find_mean_of_grades_lecturer() <= other.find_mean_of_grades_lecturer()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception('Объект не принадлежит этому классу.')
        return self.find_mean_of_grades_lecturer() == other.find_mean_of_grades_lecturer()

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress and grade in range(1,11):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"""Имя: {self.name}
        \rФамилия: {self.surname}\n"""

def find_mean_grades_of_persons(persons, course):
    if not isinstance(persons, list):
        return "Not list"
    list_grades = []
    for person in persons:
        list_grades.extend(person.grades.get(course, []))
    if not list_grades:
        return "По такому курсу ни у кого нет оценок"
    return round(sum(list_grades)/len(list_grades), 1)

best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['Git']
best_student.add_courses('Введение в программирование')

some_reviewer = Reviewer('Some', 'Buddy')
some_reviewer.courses_attached += ['Python']
some_reviewer.courses_attached += ['Git']

some_reviewer.rate_hw(best_student, 'Python', 10)
some_reviewer.rate_hw(best_student, 'Python', 10)
some_reviewer.rate_hw(best_student, 'Git', 10)
some_reviewer.rate_hw(best_student, 'Git', 9)

some_lecturer = Lecturer('Some', 'Buddy')
some_lecturer.courses_attached += ['Python']
some_lecturer.courses_attached += ['Git']

best_student.rate_lecturer_hw(some_lecturer, 'Python', 10)
best_student.rate_lecturer_hw(some_lecturer, 'Python', 10)
best_student.rate_lecturer_hw(some_lecturer, 'Git', 10)
best_student.rate_lecturer_hw(some_lecturer, 'Git', 9)

best_student_1 = Student('Ivan', 'Ivanov', 'man')
best_student_1.courses_in_progress += ['Python']
best_student_1.courses_in_progress += ['Git']
best_student_1.add_courses('Введение в программирование')
some_reviewer.rate_hw(best_student_1, 'Python', 10)
some_reviewer.rate_hw(best_student_1, 'Python', 10)
some_reviewer.rate_hw(best_student_1, 'Git', 10)
some_reviewer.rate_hw(best_student_1, 'Git', 10)


some_reviewer_1 = Reviewer('Some', 'Buddy')
some_reviewer_1.courses_attached += ['Python']
some_reviewer_1.courses_attached += ['Git']
some_reviewer_1.rate_hw(best_student, 'Python', 10)
some_reviewer_1.rate_hw(best_student, 'Python', 10)
some_reviewer_1.rate_hw(best_student_1, 'Python', 10)
some_reviewer_1.rate_hw(best_student_1, 'Python', 10)
some_reviewer_1.rate_hw(best_student, 'Git', 10)
some_reviewer_1.rate_hw(best_student, 'Git', 9)
some_reviewer_1.rate_hw(best_student_1, 'Git', 9)
some_reviewer_1.rate_hw(best_student_1, 'Git', 10)

some_lecturer_1 = Lecturer('Sim', 'Buddy')
some_lecturer_1.courses_attached += ['Python']
some_lecturer_1.courses_attached += ['Git']

best_student_1.rate_lecturer_hw(some_lecturer, 'Python', 10)
best_student_1.rate_lecturer_hw(some_lecturer, 'Python', 10)
best_student_1.rate_lecturer_hw(some_lecturer_1, 'Python', 10)
best_student_1.rate_lecturer_hw(some_lecturer_1, 'Python', 10)
best_student_1.rate_lecturer_hw(some_lecturer, 'Git', 10)
best_student_1.rate_lecturer_hw(some_lecturer, 'Git', 9)
best_student_1.rate_lecturer_hw(some_lecturer_1, 'Git', 10)
best_student_1.rate_lecturer_hw(some_lecturer_1, 'Git', 9)

best_student_2 = Student('Petr', 'Petrov', 'man')
best_student_2.courses_in_progress += ['Python']
best_student_2.courses_in_progress += ['Git']
best_student_2.add_courses('Введение в программирование')

some_reviewer_2 = Reviewer('Some', 'Buddy')
some_reviewer_2.courses_attached += ['Python']
some_reviewer_2.courses_attached += ['Git']

some_reviewer_2.rate_hw(best_student, 'Python', 10)
some_reviewer_2.rate_hw(best_student, 'Python', 10)
some_reviewer_2.rate_hw(best_student, 'Git', 10)
some_reviewer_2.rate_hw(best_student, 'Git', 9)
some_reviewer_2.rate_hw(best_student_1, 'Python', 10)
some_reviewer_2.rate_hw(best_student_1, 'Python', 10)
some_reviewer_2.rate_hw(best_student_1, 'Git', 10)
some_reviewer_2.rate_hw(best_student_1, 'Git', 9)
some_reviewer_2.rate_hw(best_student_2, 'Python', 10)
some_reviewer_2.rate_hw(best_student_2, 'Python', 10)
some_reviewer_2.rate_hw(best_student_2, 'Git', 10)
some_reviewer_2.rate_hw(best_student_2, 'Git', 9)

some_lecturer_2 = Lecturer('Sem', 'Buddy')
some_lecturer_2.courses_attached += ['Python']
some_lecturer_2.courses_attached += ['Git']

best_student.rate_lecturer_hw(some_lecturer_2, 'Python', 10)
best_student.rate_lecturer_hw(some_lecturer_2, 'Python', 10)
best_student.rate_lecturer_hw(some_lecturer_2, 'Git', 10)
best_student.rate_lecturer_hw(some_lecturer_2, 'Git', 9)
best_student_1.rate_lecturer_hw(some_lecturer_2, 'Python', 10)
best_student_1.rate_lecturer_hw(some_lecturer_2, 'Python', 10)
best_student_1.rate_lecturer_hw(some_lecturer_2, 'Git', 9)
best_student_1.rate_lecturer_hw(some_lecturer_2, 'Git', 9)
best_student_2.rate_lecturer_hw(some_lecturer_2, 'Python', 10)
best_student_2.rate_lecturer_hw(some_lecturer_2, 'Python', 9)
best_student_2.rate_lecturer_hw(some_lecturer_2, 'Git', 10)
best_student_2.rate_lecturer_hw(some_lecturer_2, 'Git', 9)


print(some_reviewer)
print(some_lecturer)
print(best_student)
print(some_reviewer_1)
print(some_lecturer_1)
print(best_student_1)
print(some_reviewer_2)
print(some_lecturer_2)
print(best_student_2)

print(best_student.__lt__(best_student_1))
print(best_student.__lt__(best_student_2))
print(best_student_1.__lt__(best_student_2))

print(some_lecturer.__lt__(some_lecturer_1))
print(some_lecturer.__lt__(some_lecturer_2))
print(some_lecturer_1.__lt__(some_lecturer_2))

print(best_student.__le__(best_student_1))
print(best_student.__le__(best_student_2))
print(best_student_1.__le__(best_student_2))

print(some_lecturer.__le__(some_lecturer_1))
print(some_lecturer.__le__(some_lecturer_2))
print(some_lecturer_1.__le__(some_lecturer_2))

print(best_student.__eq__(best_student_1))
print(best_student.__eq__(best_student_2))
print(best_student_1.__eq__(best_student_2))

print(some_lecturer.__eq__(some_lecturer_1))
print(some_lecturer.__eq__(some_lecturer_2))
print(some_lecturer_1.__eq__(some_lecturer_2))

print(find_mean_grades_of_persons([best_student, best_student_1, best_student_2],'Git'))
print(find_mean_grades_of_persons([some_lecturer, some_lecturer_1, some_lecturer_2],'Git'))