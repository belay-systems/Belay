from abc import ABC, abstractmethod


class Workflow(ABC):

    name = "Unnamed Workflow"

    description = ""

    trigger = ""

    departments = []

    @abstractmethod
    def execute(self, belay):

        pass
