from abc import ABC, abstractmethod


class Department(ABC):

    name = ""

    @abstractmethod

    def run(self, belay):

        pass
