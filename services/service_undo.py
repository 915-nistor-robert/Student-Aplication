class UndoError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ServiceUndo:
    def __init__(self, repo_undo):
        self.repo_undo = repo_undo
        self.index = -1

    def add_operation(self, operation):
        end = self.index + 1
        self.repo_undo.delete(end)
        self.repo_undo.save(operation)
        self.index += 1

    def undo(self):
        if self.index == -1:
            raise UndoError('You don\'t have any more undos')

        self.repo_undo[self.index].undo()
        self.index -= 1

    def redo(self):
        if self.index == len(self.repo_undo) - 1:
            raise UndoError('You don\'t have any more redos')

        self.index += 1
        self.repo_undo[self.index].redo()

class CascadeOperation:
    def __init__(self, *operations):
        self.operations = operations

    def undo(self):
        for operation in self.operations:
            operation.undo()

    def redo(self):
        for operation in self.operations:
            operation.redo()

class Operation:
    def __init__(self, function_call_undo, function_call_redo):
        self.function_call_undo = function_call_undo
        self.function_call_redo = function_call_redo

    def undo(self):
        self.function_call_undo()

    def redo(self):
        self.function_call_redo()

class FunctionCall:
    def __init__(self, function_reference, *function_parameters):
        self.function_reference = function_reference
        self.function_parameters = function_parameters

    def call(self):
        return self.function_reference(*self.function_parameters)

    def __call__(self):
        return self.call()