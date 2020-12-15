from domain.entity_grade import Grade
from services.service_undo import Operation, FunctionCall


class GradeService:
    def __init__(self, validator, graded_repository):
        self.__validator = validator
        self.__grades_repository = graded_repository
        # self.__ungraded_repository = ungraded_repository


    def get_graded_repository(self):
        """
        This function returns the repository of the graded homeworks
        :return: graded_repository
        """
        return self.__grades_repository
    # @property
    # def ungraded_repository(self):
    #     """
    #     This function return the repository of the ungraded homeworks
    #     :return: ungraded_repository
    #     """
    #     return self.__ungraded_repository


    # def get_ungraded_assignments(self):
    #     """
    #     This functions returns the list of the ungraded homeworks
    #     :return: self.__ungraded_repository.get_all_entities()
    #     """
    #     return self.__ungraded_repository.get_all_entities()

    def get_ungraded_assignments(self):
        grades = self.__grades_repository.get_all_entities()
        return list(filter(lambda grade: grade.grade_value == 0, grades))
        # ungraded_assignments = []
        # for grade in grades:
        #     if grade.grade_value == 'Ungraded':
        #         ungraded_assignments.append(grade)
        # return ungraded_assignments

    def get_ungraded_as_list(self):
        ungraded = self.get_ungraded_assignments()
        list_of_ungraded = []
        for grade in ungraded:
            new_grade = []
            new_grade.append(grade.assignment_id)
            new_grade.append(grade.student_id)
            new_grade.append('Ungraded')
            list_of_ungraded.append(new_grade)
        return list_of_ungraded


    def get_graded_assignments(self):
        """
        This functions returns the list of the graded homeworks
        :return:
        """
        grades = self.__grades_repository.get_all_entities()
        return list(filter(lambda grade: int(grade.grade_value) > 0, grades))
        # graded_assignments = []
        # for grade in grades:
        #     if grade.grade_value != 'Ungraded':
        #         graded_assignments.append(grade)
        # return graded_assignments

    def get_ungraded_assignments_for_a_student(self, student_id):
        """
        This function returns all the ungraded assignments one student
        :param student_id: the student's id we want to get the ungraded assignments
        :return: student_ungraded_assignments (list)
        """
        ungraded_assignments = self.get_ungraded_assignments()
        student_ungraded_assignments = []
        for assignment in ungraded_assignments:
            if assignment.student_id == student_id:
                student_ungraded_assignments.append(assignment)
        return student_ungraded_assignments

    def add_ungraded_assignment_for_student(self, assignment_id, student_id):
        """
        This function add an ungraded assignment in the list of ungraded assignments
        :param assignment_id: the id of the assignment that was given
        :param student_id: the if of the student that the assignment was given
        :return: None
        """
        ungraded_assignments = self.get_ungraded_assignments()
        grade = Grade(assignment_id, student_id, 0)
        if grade not in ungraded_assignments:
            self.__grades_repository.add_entity(grade)

        undo = FunctionCall(self.remove_grade_for_student, grade.id)
        redo = FunctionCall(self.add_ungraded_assignment_for_student, assignment_id, student_id)

        operation = Operation(undo, redo)
        return operation

    def remove_grade_for_student(self, grade_id):
        grades = self.__grades_repository.get_all_entities()
        for grade in grades:
            if grade.id == grade_id:
                # print(grades.index(grade_id))
                grade_index = self.__grades_repository.find_by_id(grade_id)
                #grades.pop(grades.index(grade_id))
                grades.pop(grade_index)

    def add_ungraded_assignment_for_group(self, assignment_id, students_in_group):
        for student in students_in_group:
            self.add_ungraded_assignment_for_student(str(assignment_id), str(student.id))

        undo = FunctionCall(self.remove_ungraded_assignment_for_group, assignment_id, students_in_group)
        redo = FunctionCall(self.add_ungraded_assignment_for_group, assignment_id, students_in_group)

        operation = Operation(undo, redo)
        return operation

    def remove_ungraded_assignment_for_group(self, assignment_id, students_in_group):
        for student in students_in_group:
            self.remove_grade_for_student(str(assignment_id) + str(student.id))

    def remove_student(self, student_id):
        """
        This functions removes all of the student's assignment, both graded and ungraded
        :param student_id: the student's id we remove
        :return:
        """
        #ungraded_assignments = self.get_ungraded_assignments()
        grades = self.__grades_repository.get_all_entities()
        #ungraded_assignments_ids_to_delete = []
        grades_ids_to_delete = []
        grades_deleted = []
        for grade in grades:
            if grade.student_id == student_id:
                grades_ids_to_delete.append(grade.id)
                grades_deleted.append(grade)

        # for grade in graded_assignments:
        #     if grade.student_id == student_id:
        #         graded_assignments_ids_to_delete.append(grade.id)

        # undo
        undo = FunctionCall(self.undo_remove, grades_deleted)
        redo = FunctionCall(self.remove_student, str(student_id))

        operation = Operation(undo, redo)

        for grade_id in grades_ids_to_delete:
            self.__grades_repository.remove_by_id(grade_id)

        return operation

        # for grade_id in graded_assignments_ids_to_delete:
        #     self.__grades_repository.remove_by_id(grade_id)

    def give_grade(self, assignment_id, student_id, grade_value):
        self.add_ungraded_assignment_for_student(assignment_id, student_id)
        self.grade_assignment(assignment_id, student_id, grade_value)

    def undo_remove(self, grades_deleted):
        # grades = self.__grades_repository.get_all_entities()
        # for grade_id in grade_ids_to_delete:
        #     grade = grades[self.__grades_repository.find_by_id(str(grade_id))]
        #     self.give_grade(grade.assignment_id, grade.student_id, grade.grade_value)
        for grade in grades_deleted:
            self.give_grade(grade.assignment_id, grade.student_id, grade.grade_value)



    def remove_assignment(self, assignment_id):
        """
        Removes all given assignment with given assignment_id , both graded and ungraded
        """
        # ungraded_assignments = self.get_ungraded_assignments()
        grades = self.__grades_repository.get_all_entities()
        # ungraded_assignments_ids_to_delete = []
        grades_ids_to_delete = []
        for grade in grades:
            if grade.assignment_id == assignment_id:
                grades_ids_to_delete.append(grade.id)

        # for grade in graded_assignments:
        #     if grade.assignment_id == assignment_id:
        #         graded_assignments_ids_to_delete.append(grade.id)

        # undo

        undo = FunctionCall(self.undo_remove, grades_ids_to_delete)
        redo = FunctionCall(self.remove_assignment, str(assignment_id))

        operation = Operation(undo, redo)

        for grade_id in grades_ids_to_delete:
            self.__grades_repository.remove_by_id(grade_id)

        # for grade_id in graded_assignments_ids_to_delete:
        #     self.__grades_repository.remove_by_id(grade_id)
        return operation


    # def undo_remove_assignment(self, grades_id_to_delete):
    #     grades = self.__grades_repository.get_all_entities()
    #     for grade_id in grades_id_to_delete:
    #         grade = grades[self.__grades_repository.find_by_id(grade_id)]


    def undo_grade_assignment(self, assignment_id, student_id):
        grade = Grade(assignment_id, student_id, 0)
        self.__grades_repository.update_entity(grade.id, grade)

    def grade_assignment(self, assignment_id, student_id, grade_value):
        """
        This functions grades an assignment
        :param assignment_id: the assignment's id we grade
        :param student_id: the student's id who has the assignment graded
        :param grade_value: the grade value
        :return:
        """
        # grades = self.__grades_repository.get_all_entities()
        # grade = grades[self.__grades_repository.find_by_id(str(assignment_id) + str(student_id))]

        # grade = Grade(assignment_id, student_id, grade_value)
        # self.__graded_repository.add_entity(grade)
        # self.__ungraded_repository.remove_by_id(grade.id)

        grade = Grade(assignment_id, student_id, grade_value)
        grade_id = str(assignment_id) + str(student_id)
        self.__grades_repository.update_entity(grade_id, grade)

        undo = FunctionCall(self.undo_grade_assignment, assignment_id, student_id)
        redo = FunctionCall(self.grade_assignment, assignment_id, student_id, grade_value)

        operation = Operation(undo, redo)
        return operation



