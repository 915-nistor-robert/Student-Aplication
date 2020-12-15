from msilib import Table
from tkinter import *
import datetime
from tkinter import messagebox

from services.service_assigment import AssignmentService
from services.service_grade import GradeService
from services.service_student import StudentService
from services.service_undo import CascadeOperation


class MenuGUI:
    def __init__(self, student_service, assignment_service, grade_service, service_statistics, service_undos, validator):
        self.frame = None
        self.window = Tk()
        self.window.geometry('370x30')
        self.__students_service = student_service
        self.__assignments_service = assignment_service
        self.__grade_service = grade_service
        self.__service_statistics = service_statistics
        self.__service_undos = service_undos
        self.__validators = validator

    # ______________________________________UI STUDENT___________________________

    def _add_student_pressed(self):
        try:
            self.__validators.validate_student(self.student_id_entry.get(), self.student_name_entry.get(),
                                               self.student_group_entry.get())
            operation = self.__students_service.add_student(int(self.student_id_entry.get()), self.student_name_entry.get(),
                                                int(self.student_group_entry.get()))
            self.__service_undos.add_operation(operation)
            messagebox.showinfo('Success', 'Student added successfully')
        except Exception as error:
            messagebox.showinfo('Error', str(error))

    def ui_add_student(self):
        add_student_window = Toplevel(self.window)
        add_student_window.geometry("500x100")
        frame = Frame(add_student_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text="Enter student's id:", font="none 12 bold").grid(row=0, column=0, sticky=W)
        self.student_id_entry = Entry(frame, width=30, bg="white")
        self.student_id_entry.grid(row=0, column=1, sticky=W)

        Label(frame, text="Enter student's name: ", font="none 12 bold").grid(row=1, column=0, sticky=W)
        self.student_name_entry = Entry(frame, width=30, bg="white")
        self.student_name_entry.grid(row=1, column=1, sticky=W)

        Label(frame, text="Enter student's group: ", font="none 12 bold").grid(row=2, column=0, sticky=W)
        self.student_group_entry = Entry(frame, width=30, bg="white")
        self.student_group_entry.grid(row=2, column=1, sticky=W)

        Button(frame, text="ADD", width=5, command=self._add_student_pressed).grid(row=3, column=0)

        self.frame = frame
        self.window.mainloop()

    def remove_student_pressed(self):
        try:
            cascade_operations_list = []
            students_repository = self.__students_service.get_students_repository()
            self.__validators.validate_student_id(self.student_id_entry.get(), students_repository)
            operation = self.__students_service.remove_student(int(self.student_id_entry.get()))
            cascade_operations_list.append(self.__grade_service.remove_student(self.student_id_entry.get()))
            cascade_operations_list.insert(0, operation)
            cascade_operation = CascadeOperation(*cascade_operations_list)
            self.__service_undos.add_operation(cascade_operation)
            messagebox.showinfo('Success', 'Student removed successfully')
        except Exception as error:
            messagebox.showinfo('Error', str(error))

    def ui_remove_student(self):
        remove_student_window = Toplevel(self.window)
        remove_student_window.geometry('500x50')
        frame = Frame(remove_student_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text="Enter student's id:", font="none 12 bold").grid(row=0, column=0, sticky=W)
        self.student_id_entry = Entry(frame, width=30, bg="white")
        self.student_id_entry.grid(row=0, column=1, sticky=W)

        Button(frame, text="REMOVE", width=6, command=self.remove_student_pressed).grid(row=1, column=0)
        self.frame = frame
        self.window.mainloop()

    def update_student_pressed(self):
        try:
            students_repository = self.__students_service.get_students_repository()
            self.__validators.validate_student_id(self.student_id_entry.get(), students_repository)
            self.__validators.validate_student(self.student_id_entry.get(), self.student_name_entry.get(),
                                               self.student_group_entry.get())
            operation = self.__students_service.update_student(int(self.student_id_entry.get()), self.student_name_entry.get(),
                                                   int(self.student_group_entry.get()))
            self.__service_undos.add_operation(operation)
            messagebox.showinfo('Success', 'Student updated successfully')
        except Exception as error:
            messagebox.showinfo('Error', str(error))

    def ui_update_student(self):
        update_student_window = Toplevel(self.window)
        update_student_window.geometry('500x100')
        frame = Frame(update_student_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text="Enter student's id:", font="none 12 bold").grid(row=0, column=0, sticky=W)
        self.student_id_entry = Entry(frame, width=30, bg="white")
        self.student_id_entry.grid(row=0, column=1, sticky=W)

        Label(frame, text="Enter new student's name: ", font="none 12 bold").grid(row=1, column=0, sticky=W)
        self.student_name_entry = Entry(frame, width=30, bg="white")
        self.student_name_entry.grid(row=1, column=1, sticky=W)

        Label(frame, text="Enter new student's group: ", font="none 12 bold").grid(row=2, column=0, sticky=W)
        self.student_group_entry = Entry(frame, width=30, bg="white")
        self.student_group_entry.grid(row=2, column=1, sticky=W)

        Button(frame, text="UPDATE", width=6, command=self.update_student_pressed).grid(row=3, column=0)
        self.frame = frame
        self.window.mainloop()

    def give_assignment_to_student_pressed(self):
        try:
            cascade_operations_list = []
            students_repository = self.__students_service.get_students_repository()
            self.__validators.validate_student_id(self.student_id_entry.get(), students_repository)
            assignments_repository = self.__assignments_service.get_assignments_repository()
            self.__validators.validate_assignment_id(self.student_id_entry.get(), assignments_repository)
            operation = self.__students_service.give_assignment_to_student(int(self.assignment_id_entry.get()),
                                                               int(self.student_id_entry.get()))
            cascade_operations_list.append(self.__grade_service.add_ungraded_assignment_for_student(self.assignment_id_entry.get(),
                                                                     self.student_id_entry.get()))
            cascade_operations_list.insert(0, operation)
            cascade_operation = CascadeOperation(*cascade_operations_list)
            self.__service_undos.add_operation(cascade_operation)

            messagebox.showinfo('Succes', 'Assignment given successfully')
        except Exception as error:
            messagebox.showinfo('Error', str(error))

    def ui_give_assignment_to_student(self):
        give_assignment_window = Toplevel(self.window)
        give_assignment_window.geometry('500x100')
        frame = Frame(give_assignment_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text="Assignment id:", font='none 12 bold').grid(row=0, column=0, sticky=W)
        self.assignment_id_entry = Entry(frame, width=30, bg="white")
        self.assignment_id_entry.grid(row=0, column=1, sticky=W)

        Label(frame, text="Student id:", font='none 12 bold').grid(row=1, column=0, sticky=W)
        self.student_id_entry = Entry(frame, width=30, bg="white")
        self.student_id_entry.grid(row=1, column=1, sticky=W)

        Button(frame, text="ASSIGN", width=6, command=self.give_assignment_to_student_pressed).grid(row=2, column=0)
        self.frame = frame
        self.window.mainloop()

    def give_assignment_to_group_pressed(self):
        try:
            cascade_operations_list = []
            students_repository = self.__students_service.get_students_repository()
            self.__validators.validate_group(self.group_entry.get(), students_repository)
            assignments_repository = self.__assignments_service.get_assignments_repository()
            self.__validators.validate_assignment_id(self.assignment_id_entry.get(), assignments_repository)
            operation = self.__students_service.give_assignment_to_group(int(self.assignment_id_entry.get()),
                                                             int(self.group_entry.get()))
            students_in_group = self.__students_service.get_group_of_students(int(self.group_entry.get()))
            cascade_operations_list.append(self.__grade_service.add_ungraded_assignment_for_group(self.assignment_id_entry.get(), students_in_group))
            cascade_operations_list.insert(0, operation)
            cascade_operation = CascadeOperation(*cascade_operations_list)
            self.__service_undos.add_operation(cascade_operation)
            messagebox.showinfo("Succes", 'Assignment given successfully')
        except Exception as error:
            messagebox.showinfo('Error', str(error))

    def ui_give_assignment_to_group(self):
        give_assignment_group_window = Toplevel(self.window)
        give_assignment_group_window.geometry('750x100')
        frame = Frame(give_assignment_group_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text="Assignment id:", font='none 12 bold').grid(row=0, column=0, sticky=W)
        self.assignment_id_entry = Entry(frame, width=30, bg="white")
        self.assignment_id_entry.grid(row=0, column=1, sticky=W)

        Label(frame, text="Group:", font='none 12 bold').grid(row=1, column=0, sticky=W)
        self.group_entry = Entry(frame, width=30, bg="white")
        self.group_entry.grid(row=1, column=1, sticky=W)

        Button(frame, text="ASSIGN", width=6, command=self.give_assignment_to_group_pressed).grid(row=2, column=0)
        self.frame = frame
        self.window.mainloop()

    def ui_list_all_students(self):
        students = self.__students_service.get_all_students()
        text = ""
        for student in students:
            text += student
            text += "\n"
        messagebox.showinfo("List student", text)

    # ___________________________________UI ASSIGNMENT_________________________________

    def add_assignment_pressed(self):
        try:
            self.__validators.validate_assignment(self.assignment_id_entry.get(), self.description_entry.get(),
                                                  self.date_entry.get())
            date = self.date_entry.get().split('.')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            deadline = datetime.date(year, month,day)
            operation = self.__assignments_service.add_assignment(int(self.assignment_id_entry.get()), self.description_entry.get(),
                                                      deadline)
            self.__service_undos.add_operation(operation)
            messagebox.showinfo('Succes', 'Assignment added successfully')
        except Exception as error:
            messagebox.showinfo("Error", str(error))

    def ui_add_assignment(self):
        add_assignment_window = Toplevel(self.window)
        add_assignment_window.geometry('500x100')
        frame = Frame(add_assignment_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text='Assignment id:', font='none 12 bold').grid(row=0, column=0, sticky=W)
        self.assignment_id_entry = Entry(frame, width=30, bg="white")
        self.assignment_id_entry.grid(row=0, column=1, sticky=W)

        Label(frame, text='Description:', font='none 12 bold').grid(row=1, column=0, sticky=W)
        self.description_entry = Entry(frame, width=30, bg='white')
        self.description_entry.grid(row=1, column=1, sticky=W)

        Label(frame, text='Deadline(YYYY/MM/DD):', font='none 12 bold').grid(row=2, column=0, sticky=W)
        self.date_entry = Entry(frame, width=30, bg='white')
        self.date_entry.grid(row=2, column=1, sticky=W)

        Button(frame, text='ADD', width=5, command=self.add_assignment_pressed).grid(row=3, column=0, sticky=W)
        self.frame = frame
        self.window.mainloop()

    def remove_assignment_pressed(self):
        try:
            cascade_operations_list = []
            assignment_repository = self.__assignments_service.get_assignments_repository()
            self.__validators.validate_assignment_id(self.assignment_id_entry.get(), assignment_repository)
            operation = self.__assignments_service.remove_assignment(int(self.assignment_id_entry.get()))
            cascade_operations_list.append(self.__grade_service.remove_assignment(self.assignment_id_entry.get()))
            cascade_operations_list.insert(0, operation)
            cascade_operation = CascadeOperation(*cascade_operations_list)
            self.__service_undos.add_operation(cascade_operation)
            messagebox.showinfo('Succes', 'Assignment removes successfully')
        except Exception as error:
            messagebox.showinfo("Error", str(error))

    def ui_remove_assignment(self):
        remove_assignment_window = Toplevel(self.window)
        remove_assignment_window.geometry('500x100')
        frame = Frame(remove_assignment_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text="Assignment id:", font="none 12 bold").grid(row=0, column=0, sticky=W)
        self.assignment_id_entry = Entry(frame, width=30, bg="white")
        self.assignment_id_entry.grid(row=0, column=1, sticky=W)

        Button(frame, text="REMOVE", width=6, command=self.remove_assignment_pressed).grid(row=1, column=0)
        self.frame = frame
        self.window.mainloop()

    def update_assignment_pressed(self):
        try:
            assignment_repository = self.__assignments_service.get_assignments_repository()
            self.__validators.validate_assignment_id(self.assignment_id_entry.get(), assignment_repository)
            self.__validators.validate_assignment(self.assignment_id_entry.get(), self.description_entry.get(),
                                                  self.date_entry.get())
            date = self.date_entry.get().split('.')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            deadline = datetime.date(year, month, day)
            operation = self.__assignments_service.update_assignment(int(self.assignment_id_entry.get()), self.description_entry.get(),
                                                         deadline)
            self.__service_undos.add_operation(operation)
            messagebox.showinfo('Succes', 'Assignment updated successfully')
        except Exception as error:
            messagebox.showinfo("Error", str(error))

    def ui_update_assignment(self):
        update_assignment_window = Toplevel(self.window)
        update_assignment_window.geometry('500x100')
        frame = Frame(update_assignment_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text='Assignment id:', font='none 12 bold').grid(row=0, column=0, sticky=W)
        self.assignment_id_entry = Entry(frame, width=30, bg="white")
        self.assignment_id_entry.grid(row=0, column=1, sticky=W)

        Label(frame, text='Description:', font='none 12 bold').grid(row=1, column=0, sticky=W)
        self.description_entry = Entry(frame, width=30, bg='white')
        self.description_entry.grid(row=1, column=1, sticky=W)

        Label(frame, text='Deadline(YYYY/MM/DD):', font='none 12 bold').grid(row=2, column=0, sticky=W)
        self.date_entry = Entry(frame, width=30, bg='white')
        self.date_entry.grid(row=2, column=1, sticky=W)

        Button(frame, text="UPDATE", width=6, command=self.update_assignment_pressed).grid(row=3, column=0)
        self.frame = frame
        self.window.mainloop()

    def ui_list_all_assignments(self):
        assignments = self.__assignments_service.get_all_assignments()
        text = ""
        for assignment in assignments:
            text += assignment
            text += '\n'
        messagebox.showinfo('List assignments', text)

    # ______________________________________UI GRADE___________________________________________

    def ui_list_all_graded_assignments(self):
        graded = self.__grade_service.get_graded_assignments()
        text = ""
        for grade in graded:
            text += str(grade)
            text += '\n'
        messagebox.showinfo("List Graded", text)

    def ui_list_all_ungraded_assignments(self):
        # ungraded = self.__grade_service.get_ungraded_as_list()
        # text = ""
        # for ungrade in ungraded:
        #     text += str(ungrade)
        #     text += '\n'
        # messagebox.showinfo("List Ungraded", text)
        # data = self.__grade_service.get_ungraded_as_list()
        # if len(data) == 0:
        #     messagebox.showinfo('Grades', 'There are no ungraded assignments in the list')
        # else:
        #     list_ungraded_window = Toplevel(self.tk)
        #     table = Table(list_ungraded_window, len(data), 3, data)
        ungraded = self.__grade_service.get_ungraded_as_list()
        text = ""
        for ungrade in ungraded:
            text += str(ungrade)
            text += '\n'
        messagebox.showinfo("List Ungraded", text)

    def grade_assignment_pressed(self):
        try:
            assignment_repository = self.__assignments_service.get_assignments_repository()
            students_repository = self.__students_service.get_students_repository()
            grades_repository = self.__grade_service.get_graded_repository()
            self.__validators.validate_student_id(self.student_id_entry.get(), students_repository)
            self.__validators.validate_assignment_id(self.assignment_id_entry.get(), assignment_repository)
            self.__validators.validate_grade(self.assignment_id_entry.get(), self.student_id_entry.get(),
                                             self.grade_value_entry.get(), grades_repository)
            operation = self.__grade_service.grade_assignment(self.assignment_id_entry.get(), self.student_id_entry.get(),
                                                  self.grade_value_entry.get())
            self.__service_undos.add_operation(operation)
            messagebox.showinfo("Succes", "Grade given successfully")
        except Exception as error:
            messagebox.showinfo("Error", str(error))

    def ui_grade_assignment(self):
        grade_assignment_window = Toplevel(self.window)
        grade_assignment_window.geometry('500x100')
        frame = Frame(grade_assignment_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text='Student id:', font='none 12 bold').grid(row=0, column=0, sticky=W)
        self.student_id_entry = Entry(frame, width=30, bg="white")
        self.student_id_entry.grid(row=0, column=1, sticky=W)

        Label(frame, text='Assignment id:', font='none 12 bold').grid(row=1, column=0, sticky=W)
        self.assignment_id_entry = Entry(frame, width=30, bg='white')
        self.assignment_id_entry.grid(row=1, column=1, sticky=W)

        Label(frame, text='Grade value:', font='none 12 bold').grid(row=2, column=0, sticky=W)
        self.grade_value_entry = Entry(frame, width=30, bg='white')
        self.grade_value_entry.grid(row=2, column=1, sticky=W)

        Button(frame, text="GRADE", width=6, command=self.grade_assignment_pressed).grid(row=3, column=0)
        self.frame = frame
        self.window.mainloop()

    # _________________________UI STATISTICS____________________________________________
    def order_students_by_an_assignment_pressed(self):
        try:
            assignment_repository = self.__assignments_service.get_assignments_repository()
            self.__validators.validate_assignment_id(self.assignment_id_entry.get(), assignment_repository)
            student_dtos = self.__service_statistics.get_students_with_given_assignment_sorted(
                int(self.assignment_id_entry.get()))
            if len(student_dtos) == 0:
                messagebox.showinfo('Statistics', 'There are no students with this assignment')
            else:
                text = ""
                for student_dto in student_dtos:
                    text += student_dto.student.name
                    text += '\n'
                messagebox.showinfo('Statistics', text)
        except Exception as error:
            messagebox.showinfo("Error", str(error))
        # graded = self.__grade_service.get_graded_assignments()
        # text = ""
        # for grade in graded:
        #     text += str(grade)
        #     text += '\n'
        # messagebox.showinfo("List Graded", text)

    def ui_order_students_by_an_assignment(self):
        order_assignment_window = Toplevel(self.window)
        order_assignment_window.geometry('500x50')
        frame = Frame(order_assignment_window, width=100, height=50)
        frame.place(x=50, y=0)
        self.frame = frame

        Label(frame, text="Assignment id:", font="none 12 bold").grid(row=0, column=0, sticky=W)
        self.assignment_id_entry = Entry(frame, width=30, bg="white")
        self.assignment_id_entry.grid(row=0, column=1, sticky=W)

        Button(frame, text="ORDER", width=6, command=self.order_students_by_an_assignment_pressed).grid(row=1, column=0)
        self.frame = frame
        self.window.mainloop()

    def ui_list_late_students(self):
        students = self.__service_statistics.get_students_with_late_assignment()
        text = ''
        for student in students:
            text += student
            text += '\n'
        messagebox.showinfo('Late students', text)

    def ui_list_best_students(self):
        students = self.__service_statistics.get_best_students()
        text = ''
        for student in students:
            text += student.student.name
            text += '\n'
        messagebox.showinfo('Late students', text)

    def ui_undo_pressed(self):
        try:
            self.__service_undos.undo()
        except Exception as error:
            messagebox.showinfo('Error', str(error))

    def ui_redo_pressed(self):
        try:
            self.__service_undos.redo()
        except Exception as error:
            messagebox.showinfo('Error', str(error))

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

    def start(self):
        # self.initialise_10_items()
        self.window.title("School application")
        menu_window = self.window
        menu_bar = Menu(menu_window)

        students_bar = Menu(menu_bar, tearoff=0)
        students_bar.add_command(label="Add student", command=self.ui_add_student)
        students_bar.add_command(label="Remove student", command=self.ui_remove_student)
        students_bar.add_command(label="Update student", command=self.ui_update_student)
        students_bar.add_command(label="Assign to student", command=self.ui_give_assignment_to_student)
        students_bar.add_command(label="Assign to group", command=self.ui_give_assignment_to_group)
        students_bar.add_separator()
        students_bar.add_command(label="List all students", command=self.ui_list_all_students)

        menu_bar.add_cascade(label="Students", menu=students_bar)

        assignments_bar = Menu(menu_bar, tearoff=0)
        assignments_bar.add_command(label="Add assignment", command=self.ui_add_assignment)
        assignments_bar.add_command(label="Remove assignment", command=self.ui_remove_assignment)
        assignments_bar.add_command(label="Update assignment", command=self.ui_update_assignment)
        assignments_bar.add_separator()
        assignments_bar.add_command(label="List assignments", command=self.ui_list_all_assignments)

        menu_bar.add_cascade(label="Assignments", menu=assignments_bar)

        grades_bar = Menu(menu_bar, tearoff=0)
        grades_bar.add_command(label="list graded assignments", command=self.ui_list_all_graded_assignments)
        grades_bar.add_command(label="list ungraded assignments", command=self.ui_list_all_ungraded_assignments)
        grades_bar.add_command(label="grade assignment", command=self.ui_grade_assignment)

        menu_bar.add_cascade(label="Grades", menu=grades_bar)

        statistics_bar = Menu(menu_bar, tearoff=0)
        statistics_bar.add_command(label="Order students by assignment",
                                   command=self.ui_order_students_by_an_assignment)
        statistics_bar.add_command(label="List students with late assignments", command=self.ui_list_late_students)
        statistics_bar.add_command(label="List best students", command=self.ui_list_best_students)

        menu_bar.add_cascade(label="Statistics", menu=statistics_bar)

        undo_button = Button(self.window, text="UNDO", command=self.ui_undo_pressed).pack(side='left')

        redo_button = Button(self.window, text="REDO", command=self.ui_redo_pressed).pack(side='right')

        self.window.config(menu=menu_bar)
        self.window.mainloop()

# students_service = StudentService()
# assignment_service = AssignmentService()
# grade_service = GradeService()
# gui = MenuGUI(students_service, assignment_service, grade_service)
# gui.start()

# frame = None
# window = Tk()
# window.geometry('370x30')
# window.mainloop()

# add_student_window = Toplevel(window)
# add_student_window.geometry("700x50")
# frame = Frame(add_student_window, width=100, height=50)
# frame.place(x=50, y=0)
# frame = frame
