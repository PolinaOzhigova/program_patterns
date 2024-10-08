from abc import ABC

from Src.Core.abstract_prototype import AbstractPrototype
from Src.Dto.filter import Filter


class NomenclaturePrototype(AbstractPrototype):

    def __init__(self, source: list):
        super().__init__(source)

    def create(self, data: list, filterDto: Filter):
        super().create(data, filterDto)
        self.data = self.filter_name(data, filterDto)
        self.data = self.filter_id(self.data, filterDto)
        instance = NomenclaturePrototype(self.data)
        return instance

    def filter_name(self, source: list, filterDto: Filter) -> list:
        if filterDto.name == "" or filterDto.name is None:
            return source
        result = []
        for item in source:
            if item.name == filterDto.name:
                result.append(item)
        return result

    def filter_id(self, source: list, filterDto: Filter) -> list:
        if filterDto.id == "" or filterDto.id is None:
            return source
        result = []
        for item in source:
            if item.name == filterDto.id:
                result.append(item)
        return result
