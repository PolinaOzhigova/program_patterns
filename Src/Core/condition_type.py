from enum import Enum

"""
Варианты сравнения
"""
class condition_type(Enum):
    EQUALS = 1
    LIKE = 2

    """
    Сформировать словарь с вариантами формата
    """
    @staticmethod
    def list():
        result = {}
        for item in condition_type:
            result[item.name] = item.value   

        return result     