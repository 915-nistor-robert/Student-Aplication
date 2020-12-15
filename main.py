import traceback
import pickle
from domain.entity_student import Student
from domain.validators import Validator
# from domain.validators_assignmentService import AssignmentValidator
# from domain.validators_gradeService import GradeValidator
# from domain.validators_studentService import StudentValidator
from repo.repo import Repository, RepositoryUndo, TextFileRepository, BinaryFileRepository
from services.service_assigment import AssignmentService
from services.service_grade import GradeService
from services.service_statistic import ServiceStatistic
from services.service_student import StudentService
from services.service_undo import ServiceUndo
from settings import Settings
from ui.console import Console
# from tests.tests import Test
from ui.gui import MenuGUI
#
# students_repository = TextFileRepository('students.txt','Student')
# assignments_repository = TextFileRepository('assignments.txt','Assignment')
# grades_repository = TextFileRepository('grades.txt','Grade')
# students = students_repository.get_all_entities()
# assignments = assignments_repository.get_all_entities()
# grades = grades_repository.get_all_entities()
# # students = [Student(100, "Ion"), Student(101, "Son")]
# # disciplines = [Discipline(100, "FP"), Discipline(101, "Sport")]
# # grades = [Grade(100, 100, 7), Grade(100, 101, 8)]
# with open('students.pickle','wb') as binary_file:
#    pickle.dump(students,binary_file)
# with open('assignments.pickle','wb') as binary_file:
#    pickle.dump(assignments,binary_file)
# with open('grades.pickle','wb') as binary_file:
#    pickle.dump(grades,binary_file)
settings = Settings('settings.properties')
repository_type, repository_students_path, assignments_repository_path, grades_repository_path, ui_type = settings.get_config_settings()

if repository_type == 'inmemory':
    students_repository = Repository()
    assignments_repository = Repository()
    grades_repository = Repository()
elif repository_type == 'textfiles':
    students_repository = TextFileRepository(repository_students_path, 'Student')
    assignments_repository = TextFileRepository(assignments_repository_path, 'Assignment')
    grades_repository = TextFileRepository(grades_repository_path, 'Grade')
else:
    students_repository = BinaryFileRepository(repository_students_path, 'Student')
    assignments_repository = BinaryFileRepository(assignments_repository_path, 'Assignment')
    grades_repository = BinaryFileRepository(grades_repository_path, 'Grade')

validator = Validator()
undo_repository = RepositoryUndo()
students_service = StudentService(validator, students_repository)
assignments_service = AssignmentService(validator, assignments_repository)
grades_service = GradeService(validator, grades_repository)
statistics_service = ServiceStatistic(students_repository, assignments_repository, grades_repository)
undo_service = ServiceUndo(undo_repository)

if repository_type == 'inmemory':
    console = Console(students_service,assignments_service,grades_service,statistics_service, undo_service, validator)
    console.initialise_10_items()
if ui_type == 'ui':
    console = Console(students_service, assignments_service, grades_service, statistics_service, undo_service,
                      validator)
    console.run_console()
else:
    interface = MenuGUI(students_service, assignments_service, grades_service, statistics_service, undo_service, validator)
    interface.start()

#
