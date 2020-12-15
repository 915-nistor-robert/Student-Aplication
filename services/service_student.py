from domain.entity_student import Student
from repo.repo import FindByIdException
from services.service_undo import FunctionCall, Operation


class StudentService:
    def __init__(self, validator, students_repository):
        self.__validator = validator
        self.__students_repository = students_repository

    @property
    def students_repository(self):
        return self.__students_repository
    
    def get_students_from_repository(self):
        return self.__students_repository.get_all_entities()

    def get_students_repository(self):
        return self.__students_repository

    def add_student(self, student_id, student_name, student_group):
        """
        this functions takes the inputs given and creates a new student with it that we want to add
        then adds it in to the students repository
        :param student_id: the student's id that needs to be added
        :param student_name: the student's name of the assignment that needs to be added
        :param student_group: the student's group of the assignment that needs to be added
        :return: None
        """

        student = Student(student_id, student_name, student_group, [])
        self.__students_repository.add_entity(student)

        undo = FunctionCall(self.remove_student, int(student_id))
        redo = FunctionCall(self.add_student, str(student_id), student_name, str(student_group))

        operation = Operation(undo, redo)
        return operation

    def undo_remove_student(self, student_id, student_name, student_group, assignments_list):
        student = Student(student_id, student_name, student_group, assignments_list)
        self.__students_repository.add_entity(student)

    def remove_student(self, student_id):
        """
        this functions deletes an student from the students repository by its id
        :param student_id: the id of the student that need to be removed
        :return: None
        """
        students = self.__students_repository.get_all_entities()
        index = self.__students_repository.find_by_id(student_id)
        student = students[index]
        self.__students_repository.remove_by_id(student_id)

        undo = FunctionCall(self.undo_remove_student, int(student.id), student.name, str(student.group), student.assignments)
        redo = FunctionCall(self.remove_student, int(student_id))

        operation = Operation(undo, redo)
        return operation

    def update_student(self, student_id, student_name, student_group):
        """
        this functions takes the inputs given and creates a new student with it that we want to update with
        then updated the old entity with the new entity in the student repository
        :param student_id: the student's id that needs to be added
        :param student_name: the student's name of the assignment that needs to be added
        :param student_group: the student's group of the assignment that needs to be added
        :return: None
        """

        student = Student(student_id, student_name, student_group, [])
        students = self.__students_repository.get_all_entities()
        index = self.__students_repository.find_by_id(student_id)
        old_student = students[index]
        self.__students_repository.update_entity(student_id, student)

        undo = FunctionCall(self.update_student, int(student_id), old_student.name, str(old_student.group))
        redo = FunctionCall(self.update_student, int(student_id), student_name, str(student_group))

        operation = Operation(undo, redo)
        return operation

    def give_assignment_to_student(self, assignment_id, student_id):
        """
        this functions finds an student by its id then assign to him an assignment
        :param assignment_id: the id of the assignment we want to give
        :param student_id: the id of the student we want to assign
        :return: None
        """

        students = self.__students_repository.get_all_entities()
        student = students[self.__students_repository.find_by_id(student_id)]
        assignments = student.assignments
        if assignment_id not in assignments:
            assignments.append(assignment_id)
        student.assignments = assignments
        self.__students_repository.update_entity(student.id, student)

        undo = FunctionCall(self.remove_assignment_from_student, (assignment_id), (student_id))
        redo = FunctionCall(self.give_assignment_to_student, (assignment_id), (student_id))

        operation = Operation(undo, redo)
        return operation

    def get_group_of_students(self, group):
        # self.__validator.validate_group(group)
        students = self.__students_repository.get_all_entities()
        students_in_group = []
        for student in students:
            if student.group == group:
                students_in_group.append(student)
        return students_in_group

    def give_assignment_to_group(self, assignment_id, group):
        """
        this functions assign an assignment to a group of students
        :param assignment_id: the id of the assignment we want to give
        :param group: the group which we want to assign
        :return: None
        """
        students = self.__students_repository.get_all_entities()
        for student in students:
            if student.group == group:
                self.give_assignment_to_student(assignment_id, student.id)

        undo = FunctionCall(self.remove_assignment_from_group, assignment_id, group)
        redo = FunctionCall(self.give_assignment_to_group, assignment_id, group)

        operation = Operation(undo, redo)
        return operation

    def remove_assignment_from_student(self, assignment_id, student_id):
        students = self.__students_repository.get_all_entities()
        student = students[self.__students_repository.find_by_id(student_id)]
        assignments = student.assignments
        if assignment_id in assignments:
            assignments.pop(assignments.index(assignment_id))
        student.assignments = assignments
        self.__students_repository.update_entity(student.id, student)

    def remove_assignment_from_group(self, assignment_id, group):
        students = self.__students_repository.get_all_entities()
        for student in students:
            if student.group == group:
                self.remove_assignment_from_student(assignment_id, student.id)

    def get_all_students(self):
        """
        return the list of student as strings
        :return: the list of student
        """
        return [str(entity) for entity in self.__students_repository.get_all_entities()]
