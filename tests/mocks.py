""" Mocks for core_main_registry_app
"""
from unittest.mock import Mock


class MockField(Mock):
    label = "mock_label"


class MockChoicesIterator(Mock):
    def __init__(self):
        super().__init__()
        self.field = MockField()
        self._idx = 0
        self.iterator_list = []

    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < len(self.iterator_list):
            self._idx += 1
            return self.iterator_list[self._idx - 1]
        else:
            raise StopIteration
