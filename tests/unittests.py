import datetime
import unittest

from domain.entity_assignment import Assignment
from domain.entity_grade import Grade
from domain.entity_student import Student
from domain.validators import Validator, InputError
# from domain.validators_assignmentService import AssignmentValidator
# from domain.validators_studentService import StudentValidator, AddException
from repo.repo import Repository, FindByIdException, RepositoryUndo
from services.SchoolSituationDTO import SchoolSituationDTO
from services.service_assigment import AssignmentService
from services.service_grade import GradeService
from services.service_statistic import ServiceStatistic
from services.service_student import StudentService
from services.service_undo import ServiceUndo, CascadeOperation, UndoError
from services.studentdto import StudentDTO


class TestStudentDTO(unittest.TestCase):
    def setUp(self):
        student = Student(1, 'Roxana', 915, [])
        grade = Grade(2, 1, 10)
        self.student_dto = StudentDTO(student, grade)

    def test_equal_student_dto(self):
        student = Student(1, 'Roxana', 915, [])
        grade = Grade(2, 1, 10)
        student_dto = StudentDTO(student, grade)
        self.assertEqual(student_dto.student.id, self.student_dto.student.id)
        self.assertEqual(student_dto.student.name, self.student_dto.student.name)
        self.assertEqual(student_dto.student.group, self.student_dto.student.group)
        self.assertEqual(student_dto.student.assignments, self.student_dto.student.assignments)

        self.assertEqual(student_dto.grade.id, self.student_dto.grade.id)
        self.assertEqual(student_dto.grade.grade_value, self.student_dto.grade.grade_value)

    def test_to_string_grade(self):
        expected_string = "(Assignment_id : 2, Student_id : 1, Grade_value : 10)"
        grade = self.student_dto.grade
        self.assertEqual(str(grade), expected_string)

    def test_to_string_student(self):
        expected_string = '(Id : 1, Name : Roxana, Group : 915, Assignments : [])'
        student = self.student_dto.student
        self.assertEqual(str(student), expected_string)

# class TestSchoolSituationDTO(unittest.TestCase):
#     def setUp(self):
#         student = Student(1, 'Robert', 915, [])
#         self.school_situation = SchoolSituationDTO(student, 6)
#
#     def test_to_string(self):
#         expected_sting = "(Id : 1, Name : Robert, Group : 915, Assignments : [])"
#         student = self.school_situation.student
#         self.assertEqual(expected_sting, str(student))


class TestRepository(unittest.TestCase):
    def setUp(self):
        self.student_repository = Repository()

    def test_find_by_id(self):
        self.assertEqual(len(self.student_repository.get_all_entities()), 0)
        student = Student('1', 'a', '12', [])
        self.student_repository.add_entity(student)
        self.assertEqual(self.student_repository.find_by_id(student.id), 0)

    def test_add_entity(self):
        self.assertEqual(len(self.student_repository.get_all_entities()), 0)
        student = Student('1', 'a', '12', [])
        self.student_repository.add_entity(student)
        self.assertEqual(len(self.student_repository.get_all_entities()), 1)
        students = self.student_repository.get_all_entities()
        self.assertEqual(students[0].id, student.id)
        self.assertEqual(students[0].name, student.name)
        self.assertEqual(students[0].group, student.group)

    def test_remove_by_id(self):
        student = Student('1', 'a', '12', [])
        self.student_repository.add_entity(student)
        self.student_repository.remove_by_id('1')
        self.assertEqual(len(self.student_repository.get_all_entities()), 0)
        self.assertRaises(FindByIdException, self.student_repository.remove_by_id, 1)

    def test_update_entity(self):
        student = Student('1', 'a', '12', [])
        self.student_repository.add_entity(student)
        student1 = Student('1', 'b', '13', [])
        self.student_repository.update_entity('1', student1)
        students = self.student_repository.get_all_entities()
        self.assertEqual(students[0].id, student1.id)
        self.assertEqual(students[0].name, student1.name)
        self.assertEqual(students[0].group, student1.group)
        self.assertRaises(FindByIdException, self.student_repository.update_entity, '2', student1)


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.validator = Validator()

    def test_validate_student(self):
        student_id = '20'
        name = 'Sinziana'
        group = '666'
        self.validator.validate_student(student_id, name, group)
        student_id = 'a12'
        self.assertRaises(InputError, self.validator.validate_student, student_id, name, group)
        student_id = '-112'
        self.assertRaises(InputError, self.validator.validate_student, student_id, name, group)
        student_id = '112'
        name = ''
        self.assertRaises(InputError, self.validator.validate_student, student_id, name, group)
        name = 'Cristian'
        group = ''
        self.assertRaises(InputError, self.validator.validate_student, student_id, name, group)
        group = '-1'
        self.assertRaises(InputError, self.validator.validate_student, student_id, name, group)

    def test_validate_assignment(self):
        assignment_id = '20'
        description = 'do stuff'
        deadline = '2020.12.24'
        self.validator.validate_assignment(assignment_id, description, deadline)
        assignment_id = '-100'
        self.assertRaises(InputError, self.validator.validate_assignment, assignment_id, description, deadline)
        assignment_id = '*00'
        self.assertRaises(InputError, self.validator.validate_assignment, assignment_id, description, deadline)
        assignment_id = '100'
        description = ''
        self.assertRaises(InputError, self.validator.validate_assignment, assignment_id, description, deadline)
        deadline = '2100.10.200'
        description = 'Write'
        self.assertRaises(InputError, self.validator.validate_assignment, assignment_id, description, deadline)
        deadline = '20000.11.32'
        self.assertRaises(InputError, self.validator.validate_assignment, assignment_id, description, deadline)
        deadline = 'a0.12.3000'
        self.assertRaises(InputError, self.validator.validate_assignment, assignment_id, description, deadline)

    def test_validate_student_id(self):
        students_repository = Repository()
        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 915, [])
        student_3 = Student(3, 'Sorin', 915, [])
        students_repository.add_entity(student_1)
        students_repository.add_entity(student_2)
        students_repository.add_entity(student_3)
        self.validator.validate_student_id('2', students_repository)
        self.assertRaises(InputError, self.validator.validate_student_id, 'a', students_repository)
        self.assertRaises(InputError, self.validator.validate_student_id, '-1', students_repository)
        self.assertRaises(InputError, self.validator.validate_student_id, '300', students_repository)

    def test_validate_assignment_id(self):
        assignment_repository = Repository()
        id = 1
        description = 'a'
        deadline = datetime.date(2020, 11, 23)
        assignment_1 = Assignment(id, description, deadline)
        assignment_repository.add_entity(assignment_1)
        id = 2
        description = 'b'
        deadline = datetime.date(2021, 11, 23)
        assignment_2 = Assignment(id, description, deadline)
        assignment_repository.add_entity(assignment_2)
        self.validator.validate_assignment_id('2', assignment_repository)
        self.assertRaises(InputError, self.validator.validate_assignment_id, 'a', assignment_repository)
        self.assertRaises(InputError, self.validator.validate_assignment_id, '-10', assignment_repository)
        self.assertRaises(InputError, self.validator.validate_assignment_id, '1000', assignment_repository)

    def test_validate_group(self):
        students_repository = Repository()
        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 915, [])
        student_3 = Student(3, 'Sorin', 915, [])
        students_repository.add_entity(student_1)
        students_repository.add_entity(student_2)
        students_repository.add_entity(student_3)
        self.validator.validate_group('915', students_repository)
        self.assertRaises(InputError, self.validator.validate_group, '-910', students_repository)
        self.assertRaises(InputError, self.validator.validate_group, 'a10', students_repository)
        self.assertRaises(InputError, self.validator.validate_group, '1000', students_repository)

    def test_validate_grade(self):
        ungraded_repository = Repository()
        grade_1 = Grade('1', '2', 0)
        grade_2 = Grade('2', '1', 0)
        grade_3 = Grade('3', '3', 0)
        ungraded_repository.add_entity(grade_1)
        ungraded_repository.add_entity(grade_2)
        ungraded_repository.add_entity(grade_3)
        self.validator.validate_grade('1', '2', '10', ungraded_repository)
        self.assertRaises(InputError, self.validator.validate_grade, 'a', '1', '3', ungraded_repository)
        self.assertRaises(InputError, self.validator.validate_grade, '1', 'a', '4', ungraded_repository)
        self.assertRaises(InputError, self.validator.validate_grade, '-1', '2', '5', ungraded_repository)
        self.assertRaises(InputError, self.validator.validate_grade, '2', '-1', '5', ungraded_repository)
        self.assertRaises(InputError, self.validator.validate_grade, '-1', '-1', '5', ungraded_repository)
        self.assertRaises(InputError, self.validator.validate_grade, '5', '20', '6', ungraded_repository)
        self.assertRaises(InputError, self.validator.validate_grade, '5', '1', '100', ungraded_repository)


class TestStudentService(unittest.TestCase):
    def setUp(self):
        student_repository = Repository()
        validator = Validator()
        self.student_service = StudentService(validator, student_repository)

    def test_getters(self):
        students_repository_prop = self.student_service.students_repository
        students_from_repository = self.student_service.get_students_from_repository()
        students_repository = self.student_service.get_students_repository()

    def test_add_student(self):
        id = '1'
        name = 'a'
        group = '15'
        self.assertEqual(len(self.student_service.get_all_students()), 0)
        self.student_service.add_student(id, name, group)
        self.assertEqual(len(self.student_service.get_all_students()), 1)
        students_repository = self.student_service.get_students_repository()
        student = students_repository.get_all_entities()
        student = student[students_repository.find_by_id(id)]
        self.assertEqual(student.id, id)
        self.assertEqual(student.name, name)
        self.assertEqual(student.group, group)

    def test_remove_student(self):
        student_id = '1'
        name = 'a'
        group = '15'
        self.student_service.add_student(student_id, name, group)
        self.assertEqual(len(self.student_service.get_all_students()), 1)
        self.student_service.remove_student(student_id)
        self.assertEqual(len(self.student_service.get_all_students()), 0)

    # self.assertRaises(FindByIdException, self.student_service.remove_student, id)

    def test_update_student(self):
        id = '1'
        name = 'a'
        group = '15'
        self.student_service.add_student(id, name, group)
        id = '1'
        name = 'b'
        group = '16'
        self.student_service.update_student(id, name, group)
        students = self.student_service.get_students_from_repository()
        self.assertEqual(students[0].id, id)
        self.assertEqual(students[0].name, name)
        self.assertEqual(students[0].group, group)
        # id = '20'
        # self.assertRaises(FindByIdException, self.student_service.update_student, id, name, group)

    def test_get_group_of_students(self):
        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        self.student_service.students_repository.add_entity(student_1)
        self.student_service.students_repository.add_entity(student_2)
        self.student_service.students_repository.add_entity(student_3)
        students_expected = [student_1, student_3]
        students_in_group = self.student_service.get_group_of_students(915)
        self.assertListEqual(students_expected, students_in_group)

    def test_give_assignment_to_student(self):
        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        self.student_service.students_repository.add_entity(student_1)
        self.student_service.students_repository.add_entity(student_2)
        self.student_service.students_repository.add_entity(student_3)
        self.student_service.give_assignment_to_student(1, 1)
        self.student_service.give_assignment_to_student(2, 1)
        self.assertEqual(len(student_1.assignments), 2)
        self.assertEqual(student_1.assignments[0], 1)
        self.assertEqual(student_1.assignments[1], 2)

    def test_give_assignment_to_group(self):
        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        self.student_service.students_repository.add_entity(student_1)
        self.student_service.students_repository.add_entity(student_2)
        self.student_service.students_repository.add_entity(student_3)
        self.student_service.give_assignment_to_group(1, 915)
        self.assertEqual(len(student_1.assignments), 1)
        self.assertEqual(len(student_3.assignments), 1)

    def test_remove_assignment_from_student(self):
        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        self.student_service.students_repository.add_entity(student_1)
        self.student_service.students_repository.add_entity(student_2)
        self.student_service.students_repository.add_entity(student_3)
        self.student_service.give_assignment_to_student(1, 1)
        self.student_service.give_assignment_to_student(2, 1)
        self.student_service.remove_assignment_from_student(1, 1)
        self.assertEqual(len(student_1.assignments), 1)
        self.assertEqual(student_1.assignments[0], 2)

    def test_remove_assignment_from_group(self):
        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        self.student_service.students_repository.add_entity(student_1)
        self.student_service.students_repository.add_entity(student_2)
        self.student_service.students_repository.add_entity(student_3)
        self.student_service.give_assignment_to_group(1, 915)
        self.student_service.remove_assignment_from_group(1, 915)
        self.assertEqual(len(student_1.assignments), 0)
        self.assertEqual(len(student_3.assignments), 0)



    # TODO give_assignment_to_student, give_assignment_to_group, remove_assignment_from_student, remove_assignment_from_group


class TestAssignmentService(unittest.TestCase):
    def setUp(self):
        assignment_repository = Repository()
        assignment_validator = Validator()
        self.assignment_service = AssignmentService(assignment_validator, assignment_repository)

    def test_getters(self):
        assignments_repository = self.assignment_service.get_assignments_repository()
        assignments_from_repository = self.assignment_service.get_assignments_from_repository()

    def test_add_assignment(self):
        id = '1'
        description = 'a'
        deadline = datetime.date(2020, 11, 23)
        self.assertEqual(len(self.assignment_service.get_assignments_from_repository()), 0)
        self.assignment_service.add_assignment(id, description, deadline)
        self.assertEqual(len(self.assignment_service.get_all_assignments()), 1)
        assignments = self.assignment_service.get_assignments_from_repository()
        self.assertEqual(assignments[0].id, id)
        self.assertEqual(assignments[0].description, description)
        self.assertEqual(assignments[0].deadline, deadline)

        self.assertRaises(FindByIdException, self.assignment_service.add_assignment, id, description, deadline)

    def test_remove_assignment(self):
        self.assertEqual(len(self.assignment_service.get_assignments_from_repository()), 0)
        id = '1'
        description = 'a'
        deadline = datetime.date(2020, 11, 23)
        self.assignment_service.add_assignment(id, description, deadline)
        self.assignment_service.remove_assignment(id)
        self.assertEqual(len(self.assignment_service.get_assignments_from_repository()), 0)
        # self.assertRaises(FindByIdException, self.assignment_service.remove_assignment, id)

    def test_update_student(self):
        id = '1'
        description = 'a'
        deadline = datetime.date(2020, 11, 23)
        self.assignment_service.add_assignment(id, description, deadline)
        id = '1'
        description = 'b'
        deadline = datetime.date(2021, 11, 23)
        self.assignment_service.update_assignment(id, description, deadline)
        assignments = self.assignment_service.get_assignments_from_repository()
        self.assertEqual(assignments[0].id, id)
        self.assertEqual(assignments[0].description, description)
        self.assertEqual(assignments[0].deadline, deadline)
        # id = '20'
        # self.assertRaises( FindByIdException , self.assignment_service.update_assignment, id, description, deadline)


class TestServiceGrade(unittest.TestCase):
    def setUp(self):
        self.students_repository = Repository()
        self.assignments_repository = Repository()

        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        self.students_repository.add_entity(student_1)
        self.students_repository.add_entity(student_2)
        self.students_repository.add_entity(student_3)

        assignment_1 = Assignment(1, 'do stuff', datetime.date(2020, 12, 24))
        assignment_2 = Assignment(2, 'do other stuff', datetime.date(2021, 12, 24))
        assignment_3 = Assignment(3, 'do more stuff', datetime.date(2019, 12, 24))
        self.assignments_repository.add_entity(assignment_1)
        self.assignments_repository.add_entity(assignment_2)
        self.assignments_repository.add_entity(assignment_3)

        grades_repository = Repository()
        validator = Validator()
        self.grades_service = GradeService(validator, grades_repository)

    def test_getters(self):
        grades_repository = self.grades_service.get_graded_repository()
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        graded_assignments = self.grades_service.get_graded_assignments()
        ungraded_assignments_list = self.grades_service.get_ungraded_as_list()

    def test_get_ungraded_assignments_for_a_student(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        ungraded_assignments = self.grades_service.get_ungraded_assignments_for_a_student(1)
        expected_assignments = self.grades_service.get_ungraded_assignments()
        self.assertListEqual(expected_assignments, ungraded_assignments)

    def test_add_ungraded_assignment_for_student(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        self.grades_service.add_ungraded_assignment_for_student(2, 1)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)
        ungraded_assignments = self.grades_service.get_ungraded_assignments_for_a_student(1)
        expected_assignments = self.grades_service.get_ungraded_assignments()
        self.assertListEqual(expected_assignments, ungraded_assignments)

    def test_remove_grade_for_student(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        ungraded_assignments_student = self.grades_service.get_ungraded_assignments_for_a_student(1)
        self.assertEqual(len(ungraded_assignments_student), 1)
        self.grades_service.remove_grade_for_student('11')
        ungraded_assignments_student = self.grades_service.get_ungraded_assignments_for_a_student(1)
        self.assertEqual(len(ungraded_assignments_student), 0)

    def test_add_ungraded_assignment_for_group(self):
        students = self.students_repository.get_all_entities()
        students_in_group = [students[0], students[2]]
        self.grades_service.add_ungraded_assignment_for_group(1, students_in_group)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)
        expected_list = []
        expected_list.append(Grade('1', '1', 0))
        expected_list.append(Grade('1', '3', 0))

        self.assertEqual(expected_list[0].id, ungraded_assignments[0].id)
        self.assertEqual(expected_list[1].id, ungraded_assignments[1].id)

    def test_remove_student(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        self.grades_service.add_ungraded_assignment_for_student(2, 1)
        self.grades_service.add_ungraded_assignment_for_student(1, 2)
        self.grades_service.grade_assignment(2, 1, 10)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)
        self.assertEqual(len(graded_assignments), 1)
        self.grades_service.remove_student(1)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(ungraded_assignments), 1)
        self.assertEqual(len(graded_assignments), 0)
        grade = Grade(1, 2, 0)
        self.assertEqual(ungraded_assignments[0].id, grade.id)

    def test_remove_assignment(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        self.grades_service.add_ungraded_assignment_for_student(2, 1)
        self.grades_service.add_ungraded_assignment_for_student(1, 2)
        self.grades_service.grade_assignment(1, 2, 10)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)
        self.assertEqual(len(graded_assignments), 1)
        self.grades_service.remove_assignment(1)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(ungraded_assignments), 1)
        self.assertEqual(len(graded_assignments), 0)
        grade = Grade('2', '1', 0)
        self.assertEqual(ungraded_assignments[0].id, grade.id)

    def test_remove_ungraded_assignment_for_group(self):
        students = self.students_repository.get_all_entities()
        students_in_group = [students[0], students[2]]
        self.grades_service.add_ungraded_assignment_for_group(1, students_in_group)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)
        self.grades_service.remove_ungraded_assignment_for_group(1, students_in_group)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 0)



    def test_grade_assignment(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        self.grades_service.add_ungraded_assignment_for_student(1, 2)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)
        self.grades_service.grade_assignment(1, 1, 10)
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(graded_assignments), 1)
        grade = Grade('1', '1', 10)
        self.assertEqual(graded_assignments[0].id, grade.id)
        self.assertEqual(graded_assignments[0].grade_value, grade.grade_value)

    def test_undo_grade_assignment(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        self.grades_service.add_ungraded_assignment_for_student(1, 2)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)
        self.grades_service.grade_assignment(1, 1, 10)
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(graded_assignments), 1)
        self.grades_service.undo_grade_assignment(1, 1)
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(graded_assignments), 0)
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 2)

    def test_give_grade(self):
        self.grades_service.give_grade(1, 1, 10)
        graded_assignments = self.grades_service.get_graded_assignments()
        self.assertEqual(len(graded_assignments), 1)
        grade = Grade('1', '1', 10)
        self.assertEqual(graded_assignments[0].id, grade.id)
        self.assertEqual(graded_assignments[0].grade_value, grade.grade_value)

    def test_undo_remove(self):
        self.grades_service.add_ungraded_assignment_for_student(1, 1)
        self.grades_service.add_ungraded_assignment_for_student(1, 2)
        self.grades_service.grade_assignment(1, 2, 10)
        grade_1 = Grade('1', '1', 0)
        grade_2 = Grade('1', '2', 10)
        self.grades_service.remove_assignment(1)
        graded_assignments = self.grades_service.get_graded_assignments()
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 0)
        self.assertEqual(len(graded_assignments), 0)
        self.grades_service.undo_remove([grade_1, grade_2])
        graded_assignments = self.grades_service.get_graded_assignments()
        ungraded_assignments = self.grades_service.get_ungraded_assignments()
        self.assertEqual(len(ungraded_assignments), 1)
        self.assertEqual(len(graded_assignments), 1)


class TestServiceStatistics(unittest.TestCase):
    def setUp(self):
        students_repository = Repository()
        assignments_repository = Repository()
        grades_repository = Repository()

        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        students_repository.add_entity(student_1)
        students_repository.add_entity(student_2)
        students_repository.add_entity(student_3)

        assignment_1 = Assignment(1, 'do stuff', datetime.date(2020, 12, 24))
        assignment_2 = Assignment(2, 'do other stuff', datetime.date(2021, 12, 24))
        assignment_3 = Assignment(3, 'do more stuff', datetime.date(2019, 12, 24))
        assignments_repository.add_entity(assignment_1)
        assignments_repository.add_entity(assignment_2)
        assignments_repository.add_entity(assignment_3)

        grade_1 = Grade('1', '1', 0)
        grade_2 = Grade('3', '3', 0)
        grade_3 = Grade('2', '1', 10)
        grade_4 = Grade('3', '2', 5)
        grade_5 = Grade('1', '3', 10)
        grade_6 = Grade('2', '2', 7)
        grades_repository.add_entity(grade_1)
        grades_repository.add_entity(grade_2)
        grades_repository.add_entity(grade_3)
        grades_repository.add_entity(grade_4)
        grades_repository.add_entity(grade_5)
        grades_repository.add_entity(grade_6)

        self.statistics_service = ServiceStatistic(students_repository, assignments_repository, grades_repository)

    def test_get_students_with_given_assignment_sorted(self):
        # print(self.statistics_service.get_assignments())
        # print(self.statistics_service.get_grades_by_assignment_id(1))
        students_list = self.statistics_service.get_students_with_given_assignment_sorted(2)
        self.assertEqual(len(students_list), 2)
        index = 0
        for student_id in [2, 1]:
            index_student = self.statistics_service.students_repository.find_by_id(student_id)
            student = self.statistics_service.students_repository.get_all_entities()
            student = student[index_student]
            grade_id = str(2) + str(student_id)
            index_grade = self.statistics_service.grades_repository.find_by_id(grade_id)
            grade = self.statistics_service.grades_repository.get_all_entities()
            grade = grade[index_grade]
            student_dto = StudentDTO(student, grade)
            stud = students_list[index]
            self.assertEqual(stud.student.id, student_dto.student.id)
            self.assertEqual(stud.student.group, student_dto.student.group)
            self.assertEqual(stud.student.name, student_dto.student.name)
            self.assertEqual(stud.grade.grade_value, student_dto.grade.grade_value)
            index += 1

    def test_get_students_with_late_assignment(self):
        students_list = self.statistics_service.get_students_with_late_assignment()
        self.assertEqual(len(students_list), 1)
        student_index = self.statistics_service.students_repository.find_by_id(3)
        student = self.statistics_service.students_repository.get_all_entities()
        student = student[student_index]
        self.assertEqual(students_list[0], student.name)

    def test_get_average_grade_of_student(self):
        average = self.statistics_service.get_average_grade_of_student(2)
        self.assertEqual(average, 6)

    def test_get_best_students(self):
        students_list = self.statistics_service.get_best_students()
        self.assertEqual(len(students_list), 3)
        index = 0
        for student_id in [1, 3, 2]:
            student_index = self.statistics_service.students_repository.find_by_id(student_id)
            student = self.statistics_service.students_repository.get_all_entities()
            student = student[student_index]
            school_situation = SchoolSituationDTO(student,
                                                  self.statistics_service.get_average_grade_of_student(student_id))
            student = students_list[index]
            self.assertEqual(school_situation.average, student.average)
            self.assertEqual(school_situation.student, student.student)
            index += 1


class TestServiceUndo(unittest.TestCase):
    def setUp(self):
        students_repository = Repository()
        assignments_repository = Repository()
        grades_repository = Repository()
        validator = Validator()
        undo_repository = RepositoryUndo()

        student_1 = Student(1, 'Robert', 915, [])
        student_2 = Student(2, 'Cristian', 914, [])
        student_3 = Student(3, 'Sorin', 915, [])
        students_repository.add_entity(student_1)
        students_repository.add_entity(student_2)
        students_repository.add_entity(student_3)

        assignment_1 = Assignment(1, 'do stuff', datetime.date(2020, 12, 24))
        assignment_2 = Assignment(2, 'do other stuff', datetime.date(2021, 12, 24))
        assignment_3 = Assignment(3, 'do more stuff', datetime.date(2019, 12, 24))
        assignments_repository.add_entity(assignment_1)
        assignments_repository.add_entity(assignment_2)
        assignments_repository.add_entity(assignment_3)

        grade_1 = Grade('1', '1', 0)
        grade_2 = Grade('3', '3', 0)
        grade_3 = Grade('2', '1', 10)
        grade_4 = Grade('3', '2', 5)
        grade_5 = Grade('1', '3', 10)
        grade_6 = Grade('2', '2', 7)
        grades_repository.add_entity(grade_1)
        grades_repository.add_entity(grade_2)
        grades_repository.add_entity(grade_3)
        grades_repository.add_entity(grade_4)
        grades_repository.add_entity(grade_5)
        grades_repository.add_entity(grade_6)

        self.students_service = StudentService(validator, students_repository)
        self.assignments_serivce = AssignmentService(validator, assignments_repository)
        self.grades_service = GradeService(validator, grades_repository)
        self.undo_service = ServiceUndo(undo_repository)

    def test_add_operation(self):
        self.assertEqual(len(self.undo_service.repo_undo), 0)
        self.assertEqual(self.undo_service.index, -1)
        operation = self.students_service.add_student(12, 'Adrian', 913)
        self.undo_service.add_operation(operation)
        self.assertEqual(len(self.undo_service.repo_undo), 1)
        self.assertEqual(self.undo_service.index, 0)
        operation = self.students_service.remove_student(3)
        cascade_list = []
        cascade_list.append(self.grades_service.remove_student('3'))
        cascade_list.insert(0, operation)
        cascade_operations = CascadeOperation(*cascade_list)
        self.undo_service.add_operation(cascade_operations)
        self.assertEqual(len(self.undo_service.repo_undo), 2)
        self.assertEqual(self.undo_service.index, 1)

    def test_undo(self):
        self.assertRaises(UndoError, self.undo_service.undo)
        operation = self.students_service.add_student(12, 'Adrian', 913)
        self.assertEqual(len(self.students_service.students_repository), 4)
        self.assertEqual(len(self.grades_service.get_graded_repository()), 6)
        self.undo_service.add_operation(operation)

        operation = self.students_service.remove_student(2)
        self.assertEqual(len(self.students_service.students_repository), 3)

        cascade_list = []
        cascade_list.append(self.grades_service.remove_student('2'))
        cascade_list.insert(0, operation)
        cascade_operation = CascadeOperation(*cascade_list)
        self.assertEqual(len(self.grades_service.get_graded_repository()), 4)
        self.undo_service.add_operation(cascade_operation)

        self.undo_service.undo()
        self.assertEqual(self.undo_service.index, 0)
        self.assertEqual(len(self.students_service.students_repository), 4)
        self.assertEqual(len(self.grades_service.get_graded_repository()), 6)

        self.undo_service.undo()
        self.assertEqual(self.undo_service.index, -1)
        self.assertEqual(len(self.students_service.students_repository), 3)

        self.assertRaises(UndoError, self.undo_service.undo)

