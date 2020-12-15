# Write an application that manages student lab assignments for a discipline. The application will store:
#
#     Student: student_id, name, group
#     Assignment: assignment_id, description, deadline
#     Grade: assignment_id, student_id, grade_value
#
# Create an application that allows to:
#
#     Manage students and assignments. The user can add, remove, update, and list both students and assignments.

class Student:
    """
    This is the class for student entity that has four attributes
    student_id - the id of the student (integer)
    student_name - the name of the student (string)
    student_group - the group number of the student (integer)
    assignments - the list of assignments of the student (list)
    """
    def __init__(self,student_id, student_name, student_group, assignments):
        self.__student_id = student_id
        self.__student_name = student_name
        self.__student_group = student_group
        self.__student_assignments = assignments

    # properties for the attributes, getters and setters
    @property
    def id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__student_name

    @name.setter
    def name(self, name):
        self.__student_name = name

    @property
    def group(self):
        return self.__student_group

    @group.setter
    def group(self, group):
        self.__student_group = group

    @property
    def assignments(self):
        return self.__student_assignments

    @assignments.setter
    def assignments(self, new_assignments):
        self.__student_assignments = new_assignments[:]

    def to_file_format(self):
        return str(self.__student_id) + ';' + str(self.name) + ';' + str(self.group)

    def __str__(self) -> str:
        return "(Id : {0}, Name : {1}, Group : {2}, Assignments : {3})".format(self.__student_id, self.__student_name, self.__student_group,
                                                                               self.__student_assignments)

