from Src.Core.abstract_prototype import abstract_prototype
from Src.Core.validator import validator, operation_exception
from Src.Core.common import common
from Src.Core.condition_type import condition_type
import abc


"""
Реализация простого прототипа на примере номенклатуры
"""
class filter_prototype(abstract_prototype):
    __maps = {}

    def __init__(self, data:list) -> None:
        validator.validate(data, list)
        self.data = data
        self.__maps[condition_type.EQUALS] = self.__equals
        self.__maps[condition_type.LIKE] =  self.__like


    def create(self, field:str, condition:condition_type, field_value ):
        validator.validate(field,str)
        validator.validate(condition, condition_type)

        if len(self.data) == 0:
            return filter_prototype(self.data)
        
        if condition not in self.__maps.keys():
            raise operation_exception(f"Тип сравнения {condition} не поддерживается!")
        
        result = []
        item = self.data[0]

        # Простой проход
        fields = common.get_fields(item, True)
        if field not in fields:
            return filter_prototype(result)

        found = list(filter(lambda x: self.__maps[condition](x, field, field_value), self.data))
        for item in found:
            result.append(item)

        # Проход по вложенным полям
        annotations = item.__annotations__
        fields = common.get_fields_models(item)
        for model_field in fields:
            found = list(filter(lambda x: f"__{model_field}" in x, annotations.keys() ))
            if len(found) > 0:
                annotation_type = annotations[found[0]]
                
                if type(annotation_type) is abc.ABCMeta:
                    type_name = annotations[found[0]].__name__
                else: 
                    type_name = annotation_type

                # Если текущий тип совпадает с типом вложенного поля
                if type_name == type(item).__name__:
                    for item in self.data:
                        value = getattr(item, model_field)
                        if self.__maps[condition](value, field, field_value):
                            result.append(item)
        
        instance = filter_prototype(result)
        return instance


    """
    Реализация полного совпадения
    """
    @staticmethod
    def __equals(item, field:str, field_value ):
        if item is None:
            return False
        
        validator.validate(field, str)
        value = getattr(item, field)

        if value == field_value:
            return True
        else:
            return False


    """
    Реализация частичного совпадения
    """
    @staticmethod
    def __like(item, field:str, field_value):
        if item is None:
            return False
        
        validator.validate(field, str)
        value = getattr(item, field)

        if field_value in value:
            return True
        else:
            return False

        