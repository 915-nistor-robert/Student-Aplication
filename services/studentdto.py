class StudentDTO:
    def __init__(self, student, grade):
        self.__student = student
        self.__grade = grade

    @property
    def student(self):
        return self.__student

    @property
    def grade(self):
        return self.__grade

    def __str__(self) -> str:
        return "Student: ( {0} , {1} , {2} ) , Grade: {3}".format(self.__student.id, self.__student.name,
                                                                   self.__student.group, self.__grade.grade_value)

