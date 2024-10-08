import abc
from Src.Core.abstact_convert import abstract_convert
from Src.Core.abstract_model import abstract_model
from Src.Core.abstract_logic import abstract_logic
from Src.Core.common import common
from Src.Core.validator import validator, operation_exception, argument_exception
from Src.Core.base_models import base_model_code, base_model_name

# Подключаем модели
from Src.Models.range import range_model
from Src.Models.group import group_model
from Src.Models.nomenclature import nomenclature_model

import datetime



"""
Конвертация в словарь простого объекта
"""
class basic_convertor(abstract_convert):
   
   """
   Сериализовать простой тип данных
   """
   def serialize(self, field: str, object) -> dict:
      super().serialize( field, object)
      
      if not isinstance(object, (int, str, bool, float)):
          self.error_text = f"Некорректный тип данных передан для конвертации. Ожидается: (int, str, bool). Передан: {type(object)}"
          return None

      try:
            return { field: object }
      except Exception as ex:
            self.set_exception(ex)  

      return None   
   
   """
   Десериализовать простой тип данных
   """
   def deserialize(self, data , field:str,  instance):
        super().deserialize(data, field, instance)
        if self.is_error: 
            return None
        
        if not isinstance(data, (int, str, bool, float)):
          self.error_text = f"Некорректный тип данных передан для конвертации. Ожидается: (int, str, bool). Передан: {type(data)}"
          return None
       
        setattr(instance, field, data)

"""
Конвертация в словарь даты
"""
class datetime_convertor(abstract_convert):
    
    def serialize(self, field: str,  object):
      
        super().serialize( field, object)

        if not isinstance(object, datetime):
          self.error_text = f"Некорректный тип данных передан для конвертации. Ожидается: datetime. Передан: {type(object)}"
          return None

        try:
            return {  field: object.strftime('%Y-%m-%d') }
        except Exception as ex:
            self.set_exception(ex)    

    def deserialize(self, data , field:str,  instance ):
        pass

"""
Конвертация в словарь ссылочного объекта
"""
class reference_convertor(abstract_convert):
    
    def serialize(self, field: str, object: abstract_model) -> dict:
        super().serialize(field, object)

        factory = convert_factory()
        return factory.serialize(object)
    
    def deserialize(self, data , field:str,  instance ):
        super().deserialize(data, field, instance)
        if self.is_error: 
            return None
        
        # Простое заполнение данными
        factory = convert_factory()
        factory.deserialize(data, instance)


"""
Фабрика для конвертиации моделей в словарь
"""    
class convert_factory(abstract_logic):
    _maps = {}
    
    def __init__(self) -> None:
        # Связка с простыми типами
        self._maps[datetime.datetime] = datetime_convertor
        self._maps[int] = basic_convertor
        self._maps[float] = basic_convertor
        self._maps[str] = basic_convertor
        self._maps[bool] = basic_convertor
        
        # Связка для всех моделей
        for  inheritor in base_model_name.__subclasses__():
            self._maps[inheritor] = reference_convertor    

        for  inheritor in base_model_code.__subclasses__():
            self._maps[inheritor] = reference_convertor        
    

    """
    Выполнить сериализацию модели в данные
    """    
    def serialize(self, object) -> dict:
        # Сконвертируем данные как список
        result = self.__convert_list("data", object)
        if result is not None:
            return result
        
        # Сконвертируем данные как значение
        result = {}
        fields = common.get_fields(object)
        
        for field in fields:
            attribute = getattr(object.__class__, field)
            if isinstance(attribute, property):
                value = getattr(object, field)
                
                # Сконвертируем данные как список
                dictionary =  self.__convert_list(field, value)
                if dictionary is None:

                    # Сконвертируем данные как значение
                    dictionary = self.__convert_item(field, value)
                    
                if len(dictionary) == 1:
                    result[field] =  dictionary[field]
                else:
                    result[field] = dictionary       
          
        return result  
    
    """
    Сконвертировать значение в словарь
    """
    def __convert_item(self, field: str,  source):
        validator.validate(field, str)
        if source is None:
            return {field: None}
        
        if type(source) not in self._maps.keys():
            self.set_exception( operation_exception(f"Не возможно подобрать конвертор для типа {type(source)}"))

        # Определим конвертор
        convertor = self._maps[ type(source)]()
        dictionary = convertor.serialize( field, source )
        
        if convertor.is_error:
            self.set_exception( operation_exception(f"Ошибка при конвертации данных {convertor.error_text}"))
        
        return  dictionary


    """
    Сконвертировать списочные значения в словарь
    """        
    def __convert_list(self, field: str,  source) -> list:
        validator.validate(field, str)
        
        # Сконвертировать список
        if isinstance(source, list):
            result = []
            for item in source:
                if isinstance(item, str | int | float | bool):
                    result.append ( item )
                else:    
                    result.append( self.__convert_item( field,  item ))  
            
            return result 
        
        # Сконвертировать словарь
        if isinstance(source, dict):
            result = {}
            for key in source:
                object = source[key]
                value = self.__convert_item( key,  object )
                result[key] = value
                
            return result    
        
        
    """
    Десериализовать один элемент
    """    
    def deserialize(self,  data:dict, instance ):
        validator.validate(data, dict)
        if instance is None:
            self.set_exception( argument_exception("Тип данных для десериализации не указан!"))
            return
        
        if type(instance) not in self._maps.keys():
            self.set_exception( operation_exception(f"Не возможно подобрать конвертор для типа {type(instance)}"))

        
        # Загрузим все простые поля
        fields = common.get_fields(instance, True)
        annotations = instance.__annotations__
        models = common.get_models()
        for field in fields:
            found_annotation = list(filter(lambda x: f"__{field}" in x, annotations.keys() ))
            found_key = list(filter(lambda x: f"{field}" in x, data.keys() ))

            if len(found_annotation) > 0 and len(found_key) > 0:
                # Модель
                annotation_type = annotations[found_annotation[0]]
                if type(annotation_type) is abc.ABCMeta:
                    type_name = annotation_type.__name__
                else: 
                    type_name =     annotation_type

                dest_data = data[found_key[0]]
                if dest_data is not None and type_name in models:
                    # Ссылочный тип
                    dest_instance = eval(f"{type_name}()")
                    convertor = self._maps[ type(instance) ]()
                    convertor.deserialize(dest_data , field,  dest_instance)
                    setattr(instance, field, dest_instance)
                elif type_name not in models:
                    convertor = self._maps[ type(dest_data) ]()
                    convertor.deserialize(dest_data , field,  instance)    

            elif len(found_annotation) == 0 and len(found_key) > 0:
                # Обычное значение
                dest_data = data[found_key[0]]
                convertor = self._maps[ type(dest_data) ]()
                convertor.deserialize(dest_data , field,  instance)
            else:
                self.set_exception( operation_exception(f"Поле {field} не имеет описание типа в модели!"))    

        # Загрузим списочные поля
        instance.deserialize(data)

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    
