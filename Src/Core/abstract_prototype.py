from abc import ABC, abstractmethod

from Src.Core.validator import validator


class AbstractPrototype(ABC):
    __data = []

    def __init__(self, source: list):
        super().__init__()
        validator.validate(source, list)
        self.__data = source

    @abstractmethod
    def create(self, data: list, filter):
        validator.validate(data, list)

        # instance = AbstractPrototype(data)
        # return instance

    @property
    def data(self) -> list:
        return self.__data

    @data.setter
    def data(self, value: list):
        self.__data = value
