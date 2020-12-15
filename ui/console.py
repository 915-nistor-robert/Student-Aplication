import datetime

from services.service_undo import CascadeOperation, UndoError


class OptionException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Console:
    """
    this class is the console of the program
    """

    def __init__(self, students_service, assignments_service, grade_service, statistics_service, service_undo,
                 validator):
        self.__students_service = students_service
        self.__validator = validator
        self.__assignments_service = assignments_service
        self.__grade_service = grade_service
        self.__statistics_service = statistics_service
        self.__service_undo = service_undo
        self.options = {'1': ('operations with students', self.ui_print_menu_students),
                        '2': ('operations with assignments', self.ui_print_menu_assignments),
                        '3': ('operations with grades', self.ui_print_menu_grades),
                        '4': ('statistics', self.ui_print_menu_statistics)

                        }
        self.students_options = {'1': ('add a student', self.ui_add_student),
                                 '2': ('remove a student', self.ui_remove_student),
                                 '3': ('update a student', self.ui_update_student),
                                 '4': ('list the students', self.print_all_students)
                                 }
        self.assignments_options = {'5': ('add an assignment', self.ui_add_assignment),
                                    '6': ('remove an assignment', self.ui_remove_assignment),
                                    '7': ('update an assigment', self.ui_update_assignment),
                                    '8': ('list the assignments', self.print_all_assignment),
                                    '9': ('give an assignment to a student', self.ui_give_assignment_to_student),
                                    '10': ('give an assignment to a group', self.ui_give_assignment_to_group)

                                    }

        self.grade_options = {'11': ('list all graded assignments', self.ui_list_graded_assignments),
                              '12': ('list all ungraded assignments', self.ui_list_ungraded_assignments),
                              '13': ('grade an assignment', self.ui_grade_assignment)

                              }

        self.statistic_options = {
            '14': ('order students by an assignment', self.ui_ordered_students_by_assignment_grade),
            '15': ('students with late assignments', self.ui_students_with_late_assignments),
            '16': ('best students', self.ui_list_best_students),
            '17': ('undo', self.ui_undo),
            '18': ('redo', self.ui_redo)

        }

    def initialise_10_items(self):
        """
        this functions initialises the list of students with 10 students
        """
        self.__students_service.add_student(1, 'Robert', 1)
        self.__students_service.add_student(2, 'Anca', 1)
        self.__students_service.add_student(3, 'Cristian', 2)
        self.__students_service.add_student(4, 'Maria', 3)
        self.__students_service.add_student(5, 'Gheorghe', 3)
        self.__students_service.add_student(6, 'Sorin', 3)
        self.__students_service.add_student(7, 'Iulian', 3)
        self.__students_service.add_student(8, 'Mihai', 3)
        self.__students_service.add_student(9, 'Orlando', 3)
        self.__students_service.add_student(10, 'Paul', 3)
        self.__assignments_service.add_assignment(1, 'make list function', datetime.date(2020, 5, 6))
        self.__assignments_service.add_assignment(2, 'make remove function', datetime.date(2021, 2, 17))
        self.__assignments_service.add_assignment(3, 'make add function', datetime.date(2020, 11, 17))
        self.__assignments_service.add_assignment(4, 'make top function', datetime.date(2020, 10, 12))
        self.__assignments_service.add_assignment(5, 'make sort function', datetime.date(2020, 12, 20))
        self.__assignments_service.add_assignment(6, 'make update function', datetime.date(2020, 10, 2))
        self.__assignments_service.add_assignment(7, 'make min function', datetime.date(2020, 12, 1))
        self.__assignments_service.add_assignment(8, 'make max function', datetime.date(2022, 1, 16))
        self.__assignments_service.add_assignment(9, 'make avg function', datetime.date(2020, 11, 20))
        self.__assignments_service.add_assignment(10, 'make winner function', datetime.date(2020, 10, 22))

    def validate_option(self, option):
        """
        this functions validates if the option given is valid
        :param option: the option of the menu
        :return:None
        :raises: OptionException if option is not in (1,10)
        """
        if int(option) not in range(1, 19):
            raise OptionException('option is not valid')

    def ui_print_menu(self):
        # print('_________________________________________________')
        # for index in range(len(self.options)):
        #     print(f'{index + 1} : {self.options[str(index + 1)][0]}')
        print('________________STUDENT_______________________')
        for option in range(1, 5):
            print(f'{option} : {self.students_options[str(option)][0]}')
        print('________________ASSIGNMENT__________________________')
        for option in range(5, 11):
            print(f'{option} : {self.assignments_options[str(option)][0]}')
        print('_________________GRADE_________________________')
        for option in range(11, 14):
            print(f'{option} : {self.grade_options[str(option)][0]}')
        print('_________________STATISTICS________________________')
        for option in range(14, 19):
            print(f'{option} : {self.statistic_options[str(option)][0]}')
        print('_________________________________________________')
        print('Type exit for quiting the program')

    def ui_print_menu_students(self):
        # for index in range(len(self.students_options)):
        #     print(f'{index + 1} : {self.students_options[str(index+1)][0]}')
        # print('_________________________________________________')
        pass

    def ui_print_menu_assignments(self):
        pass

    def ui_print_menu_grades(self):
        pass

    def ui_print_menu_statistics(self):
        pass

    def print_all_students(self):
        print(*self.__students_service.get_all_students(), sep='\n')

    def print_all_assignment(self):
        print(*self.__assignments_service.get_all_assignments(), sep='\n')

    def ui_add_student(self):
        student_id = input('enter student id: ')
        student_name = input('enter student name: ')
        student_group = input('enter student group: ')
        self.__validator.validate_student(student_id, student_name, student_group)
        operation = self.__students_service.add_student(int(student_id), student_name, int(student_group))
        self.__service_undo.add_operation(operation)
        print('Student added successfully')

    def ui_remove_student(self):
        cascade_operations_list = []
        student_id = input('enter student id: ')
        students_repository = self.__students_service.get_students_repository()
        self.__validator.validate_student_id(student_id, students_repository)
        operation = self.__students_service.remove_student(int(student_id))
        cascade_operations_list.append(self.__grade_service.remove_student(student_id))
        cascade_operations_list.insert(0, operation)
        cascade_operation = CascadeOperation(*cascade_operations_list)
        self.__service_undo.add_operation(cascade_operation)
        print('Student removed successfully')

    def ui_update_student(self):
        student_id = input('enter student id: ')
        student_name = input('enter student name: ')
        student_group = input('enter student group: ')
        self.__validator.validate_student(student_id, student_name, student_group)
        operation = self.__students_service.update_student(int(student_id), student_name, int(student_group))
        self.__service_undo.add_operation(operation)
        print('Student updated successfully')

    def ui_add_assignment(self):
        assignment_id = input('enter assignment id: ')
        assignment_description = input('enter assignment description: ')
        deadline = input('enter assignment deadline <YYYY>.<MM>.<DD> ')
        self.__validator.validate_assignment(assignment_id, assignment_description, deadline)
        date = deadline.split('.')
        year = date[0]
        month = date[1]
        day = date[2]
        # self.__assignments_validator.validate_deadline(year, month, day)
        assignment_deadline = datetime.date(int(year), int(month), int(day))
        # self.__assignments_validator.validate_add_assignment_input(assignment_id, assignment_description,
        #                                                            assignment_deadline)
        operation = self.__assignments_service.add_assignment(assignment_id, assignment_description,
                                                              assignment_deadline)
        self.__service_undo.add_operation(operation)
        print('Assignment added successfully')

    def ui_remove_assignment(self):
        cascade_operations_list = []
        assignment_id = input('enter assignment id: ')
        assignments_repository = self.__assignments_service.get_assignments_repository()
        self.__validator.validate_assignment_id(assignment_id, assignments_repository)
        # self.__assignments_validator.validate_remove_assignment_input(assignment_id)
        operation = self.__assignments_service.remove_assignment(int(assignment_id))
        cascade_operations_list.append(self.__grade_service.remove_assignment(assignment_id))
        cascade_operations_list.insert(0, operation)
        cascade_operation = CascadeOperation(*cascade_operations_list)
        self.__service_undo.add_operation(cascade_operation)
        print('Assignment removed successfully')

    def ui_update_assignment(self):
        assignment_id = input('enter assignment id: ')
        assignment_description = input('enter assignment description: ')
        deadline = input('enter assignment deadline <YYYY>.<MM>.<DD> ')
        self.__validator.validate_assignment(assignment_id, assignment_description, deadline)
        date = deadline.split('.')
        year = date[0]
        month = date[1]
        day = date[2]
        # self.__assignments_validator.validate_deadline(year, month, day)
        assignment_deadline = datetime.datetime(int(year), int(month), int(day))
        # self.__assignments_validator.validate_update_assignment_input(assignment_id, assignment_description,
        #                                                               assignment_deadline)
        operation = self.__assignments_service.update_assignment(int(assignment_id), assignment_description,
                                                                 assignment_deadline)
        self.__service_undo.add_operation(operation)
        print('Assignment updated successfully')

    def ui_give_assignment_to_student(self):
        cascade_operations_list = []
        assignment_id = input('enter assignment id: ')
        student_id = input('enter student id: ')
        students_repository = self.__students_service.get_students_repository()
        assignments_repository = self.__assignments_service.get_assignments_repository()
        self.__validator.validate_student_id(student_id, students_repository)
        self.__validator.validate_assignment_id(assignment_id, assignments_repository)
        operation = self.__students_service.give_assignment_to_student(int(assignment_id), int(student_id))
        cascade_operations_list.append(
            self.__grade_service.add_ungraded_assignment_for_student(assignment_id, student_id))
        cascade_operations_list.insert(0, operation)
        cascade_operation = CascadeOperation(*cascade_operations_list)
        self.__service_undo.add_operation(cascade_operation)
        print('Assignment given successfully')

    def ui_give_assignment_to_group(self):
        cascade_operations_list = []
        assignment_id = input('enter assignment id: ')
        group = input('enter group number: ')
        students_repository = self.__students_service.get_students_repository()
        assignments_repository = self.__assignments_service.get_assignments_repository()
        self.__validator.validate_assignment_id(assignment_id, assignments_repository)
        self.__validator.validate_group(group, students_repository)
        operation = self.__students_service.give_assignment_to_group(int(assignment_id), int(group))
        print('Assignment given successfully')
        students_in_group = self.__students_service.get_group_of_students(int(group))
        cascade_operations_list.append(
            self.__grade_service.add_ungraded_assignment_for_group(assignment_id, students_in_group))
        cascade_operations_list.insert(0, operation)
        cascade_operation = CascadeOperation(*cascade_operations_list)
        self.__service_undo.add_operation(cascade_operation)

    def ui_list_graded_assignments(self):
        grades = self.__grade_service.get_graded_assignments()
        for grade in grades:
            print(str(grade))
        print('\n')

    def ui_list_ungraded_assignments(self):
        grades = self.__grade_service.get_ungraded_assignments()
        for grade in grades:
            print(str(grade))
        print('\n')

    def ui_list_ungraded_assignments_for_a_student(self, student_id):
        print(*self.__grade_service.get_ungraded_assignments_for_a_student(student_id), sep='\n')

    def ui_grade_assignment(self):
        print('Select one of these ungraded assignments: ')
        self.ui_list_ungraded_assignments()
        student_id = input('Enter student id who\'s assignments you want to grade\n Student id :')
        if len(self.__grade_service.get_ungraded_assignments_for_a_student(student_id)) == 0:
            print('There are no more assignments to grade for this student')
        else:
            print('Select one of these ungraded assignments')
            self.ui_list_ungraded_assignments_for_a_student(student_id)
            assignment_id = input('Assignment id : ')
            grade_value = input('Grade value : ')
            grades_repository = self.__grade_service.get_graded_repository()
            self.__validator.validate_grade(assignment_id, student_id, grade_value, grades_repository)
            operation = self.__grade_service.grade_assignment(assignment_id, student_id, grade_value)
            self.__service_undo.add_operation(operation)
            print('Assignment graded successfully')

    def ui_ordered_students_by_assignment_grade(self):
        assignment_id = input('Assignment_id = ')
        print(*self.__statistics_service.get_students_with_given_assignment_sorted(int(assignment_id)), sep='\n')

    def ui_students_with_late_assignments(self):
        print(*self.__statistics_service.get_students_with_late_assignment(), sep='\n')

    def ui_list_best_students(self):
        print(*self.__statistics_service.get_best_students(), sep='\n')

    def ui_undo(self):
        try:
            self.__service_undo.undo()
        except UndoError as error:
            print(str(error))

    def ui_redo(self):
        try:
            self.__service_undo.redo()
        except UndoError as error:
            print(str(error))

    def run_console(self):
        """
        this functions runs the console and starts the program
        :return: None
        """
        while True:
            self.ui_print_menu()
            option = input('Please choose an option. \n')
            if option == 'exit':
                break
            try:
                self.validate_option(option)
                if option in ['1', '2', '3', '4']:
                    self.students_options[option][1]()
                elif option in ['5', '6', '7', '8', '9', '10']:
                    self.assignments_options[option][1]()
                elif option in ['11', '12', '13']:
                    self.grade_options[option][1]()
                else:
                    self.statistic_options[option][1]()
            except Exception as error:
                print(error)
