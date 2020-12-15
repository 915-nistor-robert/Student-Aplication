class InputError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Validator:
    def validate_student(self, student_id, student_name, student_group):
        """
                this function validate the inputs given for the add_student function : student_id, student_name, student_group
                if the inputs are correct then the functions returns nothing, otherwise it will raise custom errors
                cases for wrong inputs:
                - student_id is negative or a string
                - student_name is an integer or empty
                - student_group is negative or a string
                :param student_id: the id of the student that wants to be added
                :param student_name: the name of the student that wants to be added
                :param student_group: the group of the student that want to be added
                :return:
                :raises: AddException - if one of the inputs are invalid
                """
        if not student_id.isdigit():
            raise InputError("student's id must be a positive integer")
        if int(student_id) < 0:
            raise InputError("student's id must be a positive integer")
        if student_name == '':
            raise InputError("Student's name can't bet empty")
        if student_name.isdigit():
            raise InputError("Student's name must be a string")
        if not student_group.isdigit():
            raise InputError("Student's group must be a positive integer")
        if int(student_group) < 0:
            raise InputError("Student's group must be a positive integer")

    def validate_assignment(self, assignment_id, description, deadline):
        """
        this functions validates the input given for add_assignment function: assignment_id, description
        if the inputs are correct then the functions returns nothing, otherwise it will raise custom errors
        cases for wrong inputs:
        - assignment_id is negative or a string
        - description is a integer or empty
        :param assignment_id: the id of the assignment that needs to be added
        :param description: the description of the assignment that needs to be added
        :param deadline: the deadline of the assignment that needs to be added
        :return:
        :raises: AssignmentAddException - if one of the inputs are invalid
        """
        if not assignment_id.isdigit():
            raise InputError('id must be a positive integer')
        if int(assignment_id) < 0:
            raise InputError('id must be a positive integer')
        if description.isdigit():
            raise InputError('description must be a string')
        if description == '':
            raise InputError("description can't be empty")
        date = deadline.split('.')
        year = date[0]
        month = date[1]
        day = date[2]
        if not year.isdigit():
            raise InputError('year is not valid')
        if int(year) < 0:
            raise InputError('year is not valid')
        if not month.isdigit():
            raise InputError('month not valid')
        if int(month) not in range(1, 13):
            raise InputError('month not valid')
        if not day.isdigit():
            raise InputError('day is not valid')
        if int(day) not in range(1, 31):
            raise InputError('day is not valid')

    def validate_student_id(self, student_id, students_repository):
        if not student_id.isdigit():
            raise InputError('The student\' id must be a positive integer')
        if int(student_id) < 0:
            raise InputError('The student\' id must be a positive integer')
        if students_repository.find_by_id(int(student_id)) is None:
            raise InputError('There is no student with this id')

    def validate_assignment_id(self, assignment_id, assignment_repository):
        if not assignment_id.isdigit():
            raise InputError('The assignment\'s id must be a positive integer')
        if int(assignment_id) < 0:
            raise InputError('The assignment\'s id must be a positive integer')
        if assignment_repository.find_by_id(int(assignment_id)) is None:
            raise InputError('There is no assignment with this id')

    def validate_group(self, group, students_repository):
        if not group.isdigit():
            raise InputError('The group must be a positive integer')
        if int(group) < 0:
            raise InputError('The group must be a positive integer')

        students = students_repository.get_all_entities()
        group_exists = False
        for student in students:
            if student.group == int(group):
                group_exists = True
        if group_exists == False:
            raise InputError('There is no group with that number')

    def validate_grade(self, assignment_id, student_id, grade_value, repository_grades):
        if not assignment_id.isdigit():
            raise InputError('The assignment\'s id must be a positive integer')
        if not student_id.isdigit():
            raise InputError('The student\' id must be a positive integer')
        grade_id = str(assignment_id) + str(student_id)
        grades = repository_grades.get_all_entities()
        index = repository_grades.find_by_id(grade_id)
        if index is None:
            raise InputError('There is no grade with this id')
        grade = grades[index]
        if grade.grade_value != 0:
            raise InputError('This grade is already graded')
        if not grade_value.isdigit():
            raise InputError('Grade value must be a integer in range (1,10)')
        if int(grade_value) < 1 or int(grade_value) > 10:
            raise InputError('Grade value must be a integer in range (1,10)')

