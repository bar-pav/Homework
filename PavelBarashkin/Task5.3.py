# ### Task 4.3
# File `data/students.csv` stores information about students in [CSV]
# (https://en.wikipedia.org/wiki/Comma-separated_values) format.
# This file contains the student’s names, age and average mark.
# 1) Implement a function which receives file path and returns names of top performer students
# 2) Implement a function which receives the file path with srudents info and writes CSV student
# information to the new file in descending order of age.
# Result:
# ```
# student name,age,average mark
# Verdell Crawford,30,8.86
# Brenda Silva,30,7.53
# ...
# Lindsey Cummings,18,6.88
# Raymond Soileau,18,7.27
# ```


def get_top_performers(file_path, number_of_top_students=5):
    file_path = '../data/' + file_path
    file = open(file_path, 'r')
    file.readline()
    students = [student.rstrip().split(',') for student in file]
    file.close()
    return [student[0] for student in sorted(students, key=lambda st: (-float(st[2]), st[0]))][:number_of_top_students]


def age_desc_sort(file_path):
    file_path = '../data/' + file_path
    file = open(file_path, 'r')
    header = file.readline()
    students = [*sorted([student.rstrip().split(',') for student in file], key=lambda stud: -int(stud[1]))]
    print(students)
    file.close()
    file_sorted = open('../data/students_sorted_by_age.csv', 'w')
    file_sorted.write(header)
    file_sorted.writelines([",".join(student) + '\n' for student in students])
    file_sorted.close()


print(get_top_performers("students.csv", 5))
age_desc_sort("students.csv")
