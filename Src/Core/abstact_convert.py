
import abc
from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import validator, argument_exception


class abstract_convert(abstract_logic):
    
    """
    Сконвертировать объект в словарь
    """
    @abc.abstractmethod
    def serialize(self, field: str, object) -> dict:
        validator.validate(field, str)
        self.__error_text = ""

    """
    Сконвертировать словарь в объект
    """
    @abc.abstractmethod
    def deserialize(self, data , field: str, instance):
        validator.validate(field, str)
        if data is None:
            return None
        elif instance is None:
            raise argument_exception("Не указан тип данных для конвертации!")
        
        self.__error_text = ""    

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)        
