class SchoolSituationDTO:
    def __init__(self, student, average):
        self.__student = student
        self.__average = average

    @property
    def student(self):
        return self.__student

    @property
    def average(self):
        return self.__average

    def __str__(self) -> str:
        return "Student: ( {0} , {1} , {2} ) , Average: {3}".format(self.__student.id, self.__student.name,
                                                                   self.__student.group, self.__average)