import copy
import datetime
import pickle

from domain.entity_assignment import Assignment
from domain.entity_grade import Grade
from domain.entity_student import Student


class FindByIdException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Repository:
    def __init__(self, entities = None):
        if entities is None:
            entities = []
        self._entities = copy.deepcopy(entities)

    def __len__(self):
        return len(self._entities)

    def find_by_id(self, entity_id):
        """
        this functions searches an entity by its id, if it finds it it returns it's position
        :param entity_id: the id of the entity that need to be find
        :return: index - position of the entity found
        """
        for index, entity in enumerate(self._entities):
            if entity.id == entity_id:
                return index

    def add_entity(self, entity):
        """
        this functions add an entity to the repository
        :param entity: the entity that need to be added to the repo
        :return: None
        :raises: FindByIdException - if the id of the entity already exists
        """
        if self.find_by_id(entity.id) is not None:
            raise FindByIdException("this id already exists")
        self._entities.append(entity)

    def remove_by_id(self, entity_id):
        """
        this functions removed an entity from the repository
        :param entity_id: the id of the entity that needs to be removed
        :return: None
        :raises: FindByIdException - if the id of the entity doesn't exist
        """
        if self.find_by_id(entity_id) is None:
            raise FindByIdException("this id is non existent")
        for index, entity in enumerate(self._entities):
            if entity.id == entity_id:
                self._entities.pop(index)

    def update_entity(self, entity_id, new_entity):
        """
        this function searches an entity by its id and it updates it with a new entity
        :param entity_id: the id of the functions that need to be updated
        :param new_entity: the new entity that we want to update with
        :return: None
        :raises: FindByIdException - if the id of the entity doesn't exist
        """
        if self.find_by_id(entity_id) is None:
            raise FindByIdException("this id is non existent")
        for index, entity in enumerate(self._entities):
            if entity.id == entity_id:
                self._entities[index] = new_entity

    def get_all_entities(self):
        """
        this functions return all the entities in the repository
        :return: the list of entities
        """
        return self._entities


class RepositoryUndo:
    def __init__(self):
        self.history = []

    def save(self, operation):
        self.history.append(operation)

    def delete(self, end):
        self.history = self.history[:end]

    def __getitem__(self, position):
        return self.history[position]

    def __len__(self):
        return len(self.history)


class TextFileRepository(Repository):
    def __init__(self, file_name, entity_type) -> object:
        super().__init__()
        self._file_name = file_name
        self._entity_type = entity_type
        self.load()

    def add_entity(self, entity):
        super().add_entity(entity)
        self.save()

    def remove_by_id(self, entity_id):
        super().remove_by_id(entity_id)
        self.save()

    def update_entity(self, entity_id, entity):
        super().update_entity(entity_id, entity)
        self.save()

    def save(self):
        file_repo = open(self._file_name, 'wt')
        for entity in self._entities:
            line = entity.to_file_format()
            file_repo.write(line)
            file_repo.write('\n')
        file_repo.close()

    def load(self):
        file_repo = open(self._file_name, 'rt')
        lines = file_repo.readlines()
        file_repo.close()

        for line in lines:
            line = line.split(';')
            if self._entity_type == 'Student':
                line[2].rstrip('\n')
                super().add_entity(Student(int(line[0]), line[1], int(line[2]), []))
            elif self._entity_type == 'Assignment':
                line[2].rstrip('\n')
                line[2] = line[2].split('/')
                date = datetime.date(int(line[2][0]), int(line[2][1]), int(line[2][2]))
                super().add_entity(Assignment(int(line[0]), line[1], date))
            else:
                line[2].rstrip('\n')
                super().add_entity(Grade(int(line[0]), int(line[1]), int(line[2])))

class BinaryFileRepository(Repository):
    def __init__(self, binary_file_name, entity_type):
        super().__init__()
        self._binary_file = binary_file_name
        self._entity_type = entity_type
        self.load()

    def add_entity(self, entity):
        super().add_entity(entity)
        self.save_binary()

    def remove_by_id(self, entity_id):
        super().remove_by_id(entity_id)
        self.save_binary()

    def update_entity(self, entity_id, new_entity):
        super().update_entity(entity_id, new_entity)
        self.save_binary()

    def save_binary(self):
        file_repo = open(self._binary_file, 'wb')
        pickle.dump(self._entities, file_repo)
        file_repo.close()

    def load(self):
        file_repo = open(self._binary_file, 'rb')
        self._entities = pickle.load(file_repo)