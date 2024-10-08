from Src.Core.base_models import base_model_name
from Src.Core.validator import argument_exception, validator

"""
Модель единицы измерения
"""
class range_model(base_model_name):
    __value:int = 1
    __base:'range_model' = None

    """
    Значение 
    """
    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, value: int):
        validator.validate(value, int)
        if value <= 0:
             raise argument_exception("Некорректный аргумент!")
        self.__value = value


    """
    Базовая единица измерения
    """
    @property
    def base(self):
        return self.__base
    
    @base.setter
    def base(self, value):
        self.__base = value

    "Фабричный метод"
    @staticmethod
    def create(name:str, value:int, base = None) -> 'range_model':
        validator.validate(name, str, 255)
        validator.validate(value, int)
        
        item = range_model()
        item.name = name
        item.value = value
        if base is not None:
            item.base = base
            
        return item



