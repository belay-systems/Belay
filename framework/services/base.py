from abc import ABC, abstractmethod


class Service(ABC):

    name = ""

    @abstractmethod

    def run(self, belay):

        pass
