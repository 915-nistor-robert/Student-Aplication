class Iterable:
    class Iteration:
        def __init__(self, items):
            self._items = items
            self._position = 0

        def __next__(self):
            if self._position == len(self._items):
                raise StopIteration()

            self._position += 1
            return self._items._data[self._position - 1]

    def __init__(self):
        self._data = []

    def __iter__(self):
        return self.Iteration(self)

    def __len__(self):
        return len(self._data)

    def __delitem__(self, index):
        del self._data[index]

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def add(self, element):
        self._data.append(element)

    def getIterable(self):
        return self._data[:]
