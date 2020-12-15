from domain.entity_assignment import Assignment
from services.service_undo import FunctionCall, Operation


class AssignmentService:
    """
    this class does the functionalities that deals with assignments
    """
    def __init__(self, validator, assignments_repository):
        self.__validator = validator
        self.__assignments_repository = assignments_repository

    def get_assignments_from_repository(self):
        return self.__assignments_repository.get_all_entities()

    def get_assignments_repository(self):
        return self.__assignments_repository

    def add_assignment(self, assignment_id, description, deadline):
        """
        this functions takes the inputs given and creates a new assignment with it that we want to add
        then adds it in to the assignments repository
        :param assignment_id: the assignment_id that needs to be added
        :param description: the description of the assignment that needs to be added
        :param deadline: the deadline of the assignment that needs to be added
        :return: None
        """
        assignment = Assignment(assignment_id, description, deadline)
        self.__assignments_repository.add_entity(assignment)

        undo = FunctionCall(self.remove_assignment, str(assignment_id))
        redo = FunctionCall(self.add_assignment, str(assignment_id), description, deadline)

        operation = Operation(undo, redo)
        return operation

    def remove_assignment(self, assignment_id):
        """
        this functions deletes an assignment from the assigment repository by its id
        :param assignment_id: the id of the assignments that need to be removed
        :return: None
        """
        assignments = self.__assignments_repository.get_all_entities()
        index = self.__assignments_repository.find_by_id(assignment_id)
        assignment = assignments[index]
        self.__assignments_repository.remove_by_id(assignment_id)

        undo = FunctionCall(self.add_assignment, str(assignment.id), assignment.description, assignment.deadline)
        redo = FunctionCall(self.remove_assignment, str(assignment_id))

        operation = Operation(undo, redo)
        return operation

    def update_assignment(self,assignment_id, description, deadline):
        """
        this functions takes the inputs given and creates a new assignment with it that we want to update with
        then updates the old assignment with the given id with the new assignment created
        :param assignment_id:
        :param description:
        :param deadline:
        :return:
        """
        assignments = self.__assignments_repository.get_all_entities()
        index = self.__assignments_repository.find_by_id(assignment_id)
        old_assignment = assignments[index]
        assignment = Assignment(assignment_id, description, deadline)
        self.__assignments_repository.update_entity(assignment_id, assignment)

        undo = FunctionCall(self.update_assignment, int(old_assignment.id), old_assignment.description, old_assignment.deadline)
        redo = FunctionCall(self.update_assignment, int(assignment_id), description, deadline)

        operation = Operation(undo, redo)
        return operation

    # def grade_assignment(self, assignment_id, grade):
    #     assignments = self.__assignments_repository.get_all_entities()
    #     assignment = assignments[self.__assignments_repository.find_by_id(assignment_id)]
    #     assignment.grade = grade




    def get_all_assignments(self):
        """
        this functions returns all assignments as strings
        :return: the list of assignments
        """
        return [str(entity) for entity in self.__assignments_repository.get_all_entities()]