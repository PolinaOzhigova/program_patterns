from Src.Core.base_models import base_model_code
from Src.Core.condition_type import condition_type
from Src.Core.convert_factory import convert_factory
from Src.Core.validator import argument_exception, validator


"""
Описание одной операции фильтрации данных
"""
class filter_item(base_model_code):

    __field:str = ""
    __condition:condition_type = condition_type.EQUALS
    __value:str = ""
    

    """
    Поле по которому будем фильтровать
    """
    @property
    def field(self):
        return self.__field
    
    @field.setter
    def field(self, value:str):
        validator.validate(value, str)
        self.__field = value.strip()

    """
    Вариант сравнения
    """
    @property
    def condition(self):
        return self.__condition

    @condition.setter
    def condition(self, value:int):
        validator.validate(value, int)
        try:
            self.__condition = condition_type(value)
        except:
            raise argument_exception("Некорректно переданы параметры!")
    

    """
    Значение для фильтрации
    """
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value:str):
        validator.validate(value, str)
        self.__value = value

"""
Набор фильтров
"""        
class filter(base_model_code):
    __items:list[filter_item] = []

    @property
    def items(self) -> list[filter_item]:
        return self.__items
    
    @items.setter
    def items(self, value:list):
        validator.validate(value, list)
        self.__items = value

    """
    Дополнительный метод для десериализации
    """
    def deserialize(self, data:dict ):   
        super().deserialize(data)

        if "items" in data.keys():
            # Набор ингредиентов
            self.items.clear()
            factory = convert_factory()
            source = data["items"]    
            for item in source:
                instance = filter_item()
                factory.deserialize(item, instance)
                self.items.append( instance )
    


    """
    Шаблонный метод. Создает инстанса объекта для примера
    """
    @staticmethod
    def create_example() ->  filter:
        instance = filter()

        item1 = filter_item()
        item1.condition = condition_type.LIKE.value
        item1.field = "name"
        item1.value = "м"
        instance.items.append(item1)

        item2 = filter_item()
        item2.condition = condition_type.LIKE.value
        item2.field = "name"
        item2.value = "к"
        instance.items.append(item2)

        return instance


        





