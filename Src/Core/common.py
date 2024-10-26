import abc
from Src.Core.validator import validator, argument_exception, operation_exception
from Src.Core.base_models import base_model_code, base_model_name
from Src.Core.abstract_model import abstract_model

"""
Набор общих методов для обработки данных
"""
class common:

    """
    Получить список наименований всех моделей
    """
    @staticmethod
    def get_models() -> list:
        result = []
        for  inheritor in base_model_name.__subclasses__():
            result.append(inheritor.__name__)

        for  inheritor in base_model_code.__subclasses__():
            result.append(inheritor.__name__)

        return result    
    
    """
    Получить полный список полей любой модели
        - is_common = True - исключить из списка словари и списки
    """
    @staticmethod
    def get_fields(source, is_common: bool = False) -> list:
        if source is None:
            raise argument_exception("Некорректно переданы аргументы!")
        
        items = list(filter(lambda x: not x.startswith("_") , dir(source))) 
        result = []
        
        for item in items:
            attribute = getattr(source.__class__, item)
            if isinstance(attribute, property):
                value = getattr(source, item)

                # Флаг. Только простые типы и модели включать
                if is_common == True and (isinstance(value, dict) or isinstance(value, list) ):
                    continue

                result.append(item)
                    
        return result
    
    """
    Получить список полей в которых включена модель данных
    """
    def get_fields_models(source) -> list:
        models = common.get_models()
        items = list(filter(lambda x: not x.startswith("_") , dir(source))) 
        annotations = source.__annotations__
        result = []
        
        for item in items:
            attribute = getattr(source.__class__, item)
            if isinstance(attribute, property):
                value = getattr(source, item)

                # Откинем лишнее
                if (isinstance(value, dict) or isinstance(value, list)):
                    continue

                # Проверим по значению        
                if isinstance(value, base_model_code) or isinstance( value, base_model_name):
                    result.append(item )
                    continue

                # Проверим по описанию
                found = list(filter(lambda x: f"__{item}" in x, annotations.keys() ))
                if len(found) > 0:
                    annotation_type = annotations[found[0]]
                    if type(annotation_type) is abc.ABCMeta:
                        type_name = annotations[found[0]].__name__
                    else: 
                        type_name =     annotation_type

                    if type_name in models:
                        result.append(item )
                        continue

                    
        return result

  




