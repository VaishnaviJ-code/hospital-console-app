from abc import ABC, abstractmethod

class TestDaoService(ABC):

    @abstractmethod
    def add_test(self, test):
        pass

    @abstractmethod
    def display_tests(self):
        pass
