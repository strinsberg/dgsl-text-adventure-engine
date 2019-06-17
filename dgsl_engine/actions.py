from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def execute(self, player):
        pass


class Get(Action):
    def execute(self, player):
        pass


class Use(Action):
    pass


class Quit(Action):
    pass