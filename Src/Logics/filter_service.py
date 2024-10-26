
from Src.Core.abstract_logic import abstract_logic
from Src.Logics.filter_prototype import filter_prototype
from Src.Dto.filter import filter
from Src.Core.validator import validator


"""
Сервис для фильтрации данных
"""
class filter_service(abstract_logic):

    """
    Выполнить фильтрацию данных
    """
    def filter(self, data:list, filterDto: filter):
        validator.validate(data, list)
        validator.validate(filterDto, filter)

        prototype = filter_prototype(data)
        for item in filterDto.items:
            prototype = prototype.create(item.field, item.condition, item.value)

        # Получить результат
        return prototype.data


    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    
        

    