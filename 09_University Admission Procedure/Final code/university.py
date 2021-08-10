from numpy import mean

MATH, PHYSICS, BIOTECH, CHEM, ENGINEERING = DEP_NAMES = "Mathematics", "Physics", "Biotech", "Chemistry", "Engineering"
PHYSICS_EX, CHEMISTRY_EX, MATH_EX, CS_EX, SPECIAL_EX = "physics_ex", "chemistry_ex", "math_ex", "cs_ex", "special_ex"

ADDRESS = "/Users/roger/Library/Mobile Documents/com~apple~CloudDocs/Downloads/applicant_list_7.txt"

DEP_EXAM = {MATH: MATH_EX, PHYSICS: (PHYSICS_EX, MATH_EX), BIOTECH: (CHEMISTRY_EX, PHYSICS_EX), CHEM: CHEMISTRY_EX,
            ENGINEERING: (CS_EX, MATH_EX)}

FILE = open(ADDRESS)

# the input will stay like this i think
MAX_N_ACCEPTED = int(input())


# --------------------classes-------------------------------------------classes-----------------------
class Student:
    def __init__(self, student_line: str):
        self.exams = {}
        self.first_n, self.last_n, self.exams[PHYSICS_EX], self.exams[CHEMISTRY_EX], self.exams[MATH_EX], self.exams[
            CS_EX], self.exams[SPECIAL_EX], self.first_dep, self.second_dep, self.third_dep = student_line.split()
        # exams to float ---ignore the yellow underlining
        value: str
        self.exams = {key: float(value) for key, value in self.exams.items()}

    def get_exam_of(self, dep):
        exams_for_dep = DEP_EXAM[dep.name]
        if type(exams_for_dep) is tuple:
            exam = mean([self.exams[exams_for_dep[0]], self.exams[exams_for_dep[1]]])
        else:
            exam = self.exams[DEP_EXAM[dep.name]]
        exam = self.exams[SPECIAL_EX] if exam < self.exams[SPECIAL_EX] else exam
        return exam

    # TODO for now I simply deleted the gpa, later i should use the dep_exam dict to select which exam score to retrieve
    def full_name(self, dep=None) -> str:
        if dep:
            return " ".join([self.first_n, self.last_n, str(self.get_exam_of(dep))])
        else:
            return " ".join([self.first_n, self.last_n])

    # shows all properties for the debugger
    def __repr__(self):
        return " ".join(
            [self.first_n, self.last_n, self.exams.items(), self.first_dep, self.second_dep, self.third_dep])


class Department:
    def __init__(self, name: str, max_students: int):
        self.name = name
        self.max_students = max_students
        self.enrolled_students = []
        self.curr_dep_ranking = []

    def __str__(self):
        return self.name

    def enroll_student(self, student: Student):
        self.enrolled_students.append(student)

    def add_student_to_ranking(self, all_students: list[Student], round_n: int):
        for student in all_students:
            # below checks the round to match student preference with department
            curr_dep_name = student.first_dep if round_n == 1 else (
                student.second_dep if round_n == 2 else student.third_dep)
            if curr_dep_name == self.name:
                self.curr_dep_ranking.append(student)

    def get_available_places(self):
        return self.max_students - len(self.enrolled_students)

    def enroll_ranking(self):
        for rank_number in range(self.get_available_places()):
            if rank_number < len(self.curr_dep_ranking):
                self.enroll_student(self.curr_dep_ranking[rank_number])
        for student in self.enrolled_students:
            if student in self.curr_dep_ranking:
                self.curr_dep_ranking.remove(student)


# --------------------classes-------------------------------------------classes-----------------------


# --------------------functions-------------------------------------------functions-----------------------
def main():
    free_students = get_students()
    deps = set_departments()
    for round_n in range(1, 4):
        deps = get_rank_of_every_dep(deps, free_students, round_n)
        deps = get_round_enrolled_deps(deps)
        enrolled_studs = get_enrolled_studs(free_students, deps)
        free_students = [student for student in free_students if student not in enrolled_studs]
    prov_print_studs(free_students, deps)
    create_files(deps)


# returns list of students converted into Student objects
def get_students() -> list:
    student_list = [Student(student_line) for student_line in FILE.readlines()]
    return student_list


# creates the Department objects
def set_departments() -> list:
    departments = [Department(dep_name, MAX_N_ACCEPTED) for dep_name in DEP_NAMES]
    return departments


# takes a dep, and sorts its enrolled students or curr_ranking, returns the dep
def get_sorted_list_of_studs(dep: Department, enrolled_students: bool) -> Department:
    if enrolled_students:
        dep.enrolled_students = sorted(dep.enrolled_students,
                                       key=lambda stud: (-stud.get_exam_of(dep), stud.full_name()))
    else:
        dep.curr_dep_ranking = sorted(dep.curr_dep_ranking, key=lambda stud: (-stud.get_exam_of(dep), stud.full_name()))
    return dep


def get_rank_of_every_dep(deps: list[Department], all_students: list[Student], round_n):
    for dep in deps:
        dep.add_student_to_ranking(all_students, round_n)
        dep = get_sorted_list_of_studs(dep, enrolled_students=False)
        # TODO change dep.curr_dep for only dep and add arg(bool) for the list to sort, delete round_n
    return deps


def get_round_enrolled_deps(deps: list[Department]):
    for dep in deps:
        dep.enroll_ranking()
        dep = get_sorted_list_of_studs(dep, enrolled_students=True)
    return deps


# returns list of enrolled students
def get_enrolled_studs(all_students: list[Student], deps: list[Department]):
    enrolled = [student for dep in deps for student in dep.enrolled_students]
    return enrolled


# provisional print all students
def prov_print_studs(studs: list[Student], deps: list[Department]):
    # for stud in studs:
    #    prints all the info of the rejected students
    #    print(stud.exams, stud.full_name(), stud.first_dep, stud.second_dep, stud.third_dep)
    deps = sorted(deps, key=lambda dept: dept.name)
    for dep in deps:
        # prints full name and score of the exam that got them in
        print(f"\n\n{dep}")
        for stud in dep.enrolled_students:
            print(stud.full_name(), stud.get_exam_of(dep))


# function to create the files
def create_files(deps: list[Department]):
    deps = sorted(deps, key=lambda dept: dept.name)
    for dep in deps:
        file = open(f'{dep.name.casefold()}.txt', 'w')
        file.writelines([stud.full_name(dep) + "\n" for stud in dep.enrolled_students])
        file.close()


# --------------------functions-------------------------------------------functions-----------------------


# --------------------code execution-----------------------
main()

FILE.close()
# --------------------code execution-----------------------
