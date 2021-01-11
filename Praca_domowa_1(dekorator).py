from time import sleep, time

def count_time(func):
    def decorator(*args, **kwargs):
        s = time()
        print('.'*20)
        func(*args, **kwargs)
        print('-'*20)
        e = time()
        print('Time elapsed: {:.1}'.format(e-s))
    return decorator

@count_time
def print_students_names(students):
    for student in students:
        print(f'Imię studenta: {student}')

@count_time
def print_students_info(students, students_indices):
    for student, index in zip(students, students_indices):
        print(f'Imię studenta: {student}, indeks {index}')

students = ['Jan', 'Maria']
indices = [111001, 111002]
print_students_names(students)
print_students_info(students, indices)

