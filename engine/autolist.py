from collections.abc import Sequence

class AutoList(Sequence):
    def __init__(self, func=None):
        super().__init__()

        self._generator = func

        self.__repopulate()

    def __getitem__(self, idx):
        return self._values[idx]

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        self.__repopulate()
        return iter(self._values)

    def __repr__(self):
        return str(self._values)

    def __repopulate(self):
        if self._generator:
            self._values = self._generator()
