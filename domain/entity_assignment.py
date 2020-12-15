


class Assignment:
    """
    This is the class for the assignment entity that has three attributes:
    assignment_id - the id of the assignment (integer)
    description - the description of the assignment (string)
    deadline - the deadline of the assignment (datetime object)
    """
    def __init__(self,assigment_id, description, deadline):
        self.__assigment_id = assigment_id
        self.__description = description
        self.__deadline = deadline


    # properties for the attributes, getters and setters
    @property
    def id(self):
        return self.__assigment_id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        self.__description = description

    @property
    def deadline(self):
        return self.__deadline

    @deadline.setter
    def deadline(self, deadline):
        self.__deadline = deadline

    def to_file_format(self):
        return str(self.__assigment_id) + ';' + str(self.description) + ';' + self.deadline.strftime('%Y/%m/%d')



    def __str__(self) -> str:
        return "({0},{1},{2})".format(self.__assigment_id, self.__description, self.__deadline)
