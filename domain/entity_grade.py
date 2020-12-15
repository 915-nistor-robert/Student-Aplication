

class Grade:
    def __init__(self, assignment_id, student_id, grade_value):
        self.__grade_id = str(assignment_id) + str(student_id)
        self.__assignment_id = assignment_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def id(self):
        return self.__grade_id

    @property
    def assignment_id(self):
        return self.__assignment_id

    @property
    def student_id(self):
        return self.__student_id

    @property
    def grade_value(self):
        return self.__grade_value

    @grade_value.setter
    def grade_value(self, value):
        self.__grade_value = value

    def to_file_format(self):
        return str(self.__assignment_id) + ';' + str(self.__student_id) + ';' + str(self.__grade_value)

    def __str__(self) -> str:
        if self.__grade_value == 0:
            grade_value = 'Ungraded'
        else:
            grade_value = self.__grade_value
        return "(Assignment_id : {0}, Student_id : {1}, Grade_value : {2})".format(self.__assignment_id, self.__student_id, grade_value)
