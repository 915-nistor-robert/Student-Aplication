import datetime

from iterable.functions import Function
from services.SchoolSituationDTO import SchoolSituationDTO
from services.studentdto import StudentDTO


class ServiceStatistic:
    def __init__(self, students_repository, assignments_repository, grades_repository):
        self.__students_repository = students_repository
        self.__assignments_repository = assignments_repository
        # self.__ungraded_repository = ungraded_repository
        self.__grades_repository = grades_repository
        self.__functions = Function()

    def get_students(self):
        return self.__students_repository.get_all_entities()

    def get_assignments(self):
        return self.__assignments_repository.get_all_entities()

    def get_grades(self):
        return self.__grades_repository.get_all_entities()

    @property
    def students_repository(self):
        return self.__students_repository

    @property
    def assignments_repository(self):
        return self.__assignments_repository

    @property
    def grades_repository(self):
        return self.__grades_repository

    # def get_ungraded(self):
    #     return self.__ungraded_repository.get_all_entities()
    @staticmethod
    def criteria_graded(grade,parameter):
        if grade.grade_value > 0:
            return True
        return False


    def get_graded(self):
        return self.__functions.filter(self.get_grades(),self.criteria_graded)

    @staticmethod
    def criteria_ungraded(grade, parameter):
        if grade.grade_value == 0:
            return True
        return False



    def get_ungraded(self):
        return self.__functions.filter(self.get_grades(), self.criteria_ungraded)

    @staticmethod
    def criteria_by_assignment_id(grade, assignment_id):
        if grade.assignment_id == assignment_id:
            return True
        return False

    def filter_grades_by_assignment_id(self, assignment_id):
        filtered_list = self.__functions.filter(self.get_graded(), self.criteria_by_assignment_id, assignment_id)
        return filtered_list[:]

    @staticmethod
    def criteria_by_student_id(grade, assignment_id):
        if grade.student_id == assignment_id:
            return True
        return False

    def filter_grades_by_student_id(self, student_id):
        filtered_list = self.__functions.filter(self.get_graded(), self.criteria_by_student_id, student_id)
        return filtered_list[:]

    @staticmethod
    def sort_ascending_grades(student_dto1, student_dto2):
        if student_dto1.grade.grade_value <= student_dto2.grade.grade_value:
            return True
        return False


    def get_students_with_given_assignment_sorted(self, assignment_id):
        """
        This function returns all the students sorted who has the assignment given
        :param assignment_id:
        :return:
        """
        students_with_given_assignment = []
        grades = self.filter_grades_by_assignment_id(assignment_id)
        for grade in grades:
            student = self.__students_repository.get_all_entities()
            student = student[self.__students_repository.find_by_id(int(grade.student_id))]
            studentDTO = StudentDTO(student, grade)
            students_with_given_assignment.append(studentDTO)

        return self.__functions.gnome_sort(students_with_given_assignment, self.sort_ascending_grades)

        # students_with_given_assignment = []
        # grades = self.get_grades_by_assignment_id(assignment_id)
        # for grade in grades:
        #     student = self.__students_repository.get_all_entities()
        #     student = student[self.__students_repository.find_by_id(int(grade.student_id))]
        #     studentDTO = StudentDTO(student, grade)
        #     students_with_given_assignment.append(studentDTO)
        # return sorted(students_with_given_assignment, key=lambda studentDTO: studentDTO.grade.grade_value)
        # students_with_give_assignment = []
        # students = self.__students_repository.get_all_entities()
        # graded_assignments = self.__graded_repository.get_all_entities()
        # students = []
        # filtered_grades_by_assignment_id = self.get_grades_by_assignment_id(assignment_id)
        # sorted_grades = filtered_grades_by_assignment_id.sort(key=)

    # def order_students_by_grade_of_assignment(self, assignment_id):
    #     students_with_given_assignment = self.get_students_with_given_assignment(assignment_id)
    #     graded_students = []
    #     graded_assignments = self.__graded_repository.get_all_entities()
    #     for student in students_with_given_assignment:


    @staticmethod
    def criteria_deadline(grade, assignments_repository):
        today_date = datetime.date.today()
        index = assignments_repository.find_by_id(int(grade.assignment_id))
        assignment = assignments_repository.get_all_entities()
        assignment = assignment[index]
        if assignment.deadline < today_date:
            return True
        return False




    def get_students_with_late_assignment(self):
        """
        :return: the list of the names of the students with late assignments
        """
        list_of_students = []
        ungraded = self.get_ungraded()
        ungraded = self.__functions.filter(ungraded, self.criteria_deadline, self.assignments_repository)
        # print(ungraded)
        for grade in ungraded:
            student = self.__students_repository.get_all_entities()
            student = student[self.__students_repository.find_by_id(int(grade.student_id))]
            list_of_students.append(student.name)
        # print(list_of_students)
        return list_of_students

    # def get_grades_by_student_id(self, student_id):
    #     """
    #     :param student_id:
    #     :return: the list of grades for a given student
    #     """
    #     # grades = list(filter(lambda grade: grade.student_id == str(student_id) , self.get_graded()))
    #     grades = []
    #     graded_assignments = self.get_graded()
    #     for grade in graded_assignments:
    #         if grade.student_id == str(student_id):
    #             grades.append(grade)
    #     return grades[:]

    # def get_grades_by_assignment_id(self, assignment_id):
    #     """
    #     :param assignment_id:
    #     :return: the list of grades for a given assignment
    #     """
    #     # grades = list(filter(lambda grade: grade.assignment_id == assignment_id, self.get_graded()))
    #     grades = []
    #     graded_assignments = self.get_graded()
    #     for grade in graded_assignments:
    #         if grade.assignment_id == str(assignment_id):
    #             grades.append(grade)
    #     return grades[:]
    @staticmethod
    def sort_descending_avergaes(school_situation1, school_situation2):
        if school_situation1.average >= school_situation2.average:
            return True
        return False

    def get_average_grade_of_student(self, student_id):
        """
        :param student_id:
        :return: the average grade of a student
        """
        grades = self.filter_grades_by_student_id(student_id)
        sum_grades = sum(int(grade.grade_value) for grade in grades)
        return sum_grades / len(grades)

    def get_best_students(self):
        """
        :return: the list of students sorted by the average grade
        """
        students = self.get_students()
        students_average = []
        students_school_situation = []
        # for student in students:
        #     average = (self.get_average_grade_of_student(student.id), student.id)
        #     students_average.append(average)
        # students_average.sort(reverse=True)
        # sorted_students = []
        # for average in students_average:
        #     student = students[self.__students_repository.find_by_id(average[1])]
        #     sorted_students.append(student)
        # return sorted_students
        for student in students:
            if len(self.filter_grades_by_student_id(student.id)) != 0:
                average = self.get_average_grade_of_student(student.id)
                student_school_situation_dto = SchoolSituationDTO(student, average)
                students_school_situation.append(student_school_situation_dto)
        return self.__functions.gnome_sort(students_school_situation, self.sort_descending_avergaes)
        # return sorted(students_school_situation,
        #               key=lambda student_school_situation_dto: student_school_situation_dto.average, reverse=True)
