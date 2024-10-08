

from Src.Core.base_models import base_model_code
from Src.Core.validator import argument_exception, validator
from Src.Models.nomenclature import nomenclature_model
from Src.Models.range import range_model


"""
Модель ингредиента
"""
class ingredient_model(base_model_code):
    __range: range_model = None
    __nomenclature: nomenclature_model = None
    __quantity:int = 0

    """
    Номенклатура
    """
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature
    

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    """
    Единица измерения
    """
    @property
    def range(self) -> range_model:
        return self.__range
    
    @range.setter
    def range(self, value:range_model):
        validator.validate(value, range_model)
        self.__range = value

    """
    Количество
    """
    @property
    def quantity(self) -> int:
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value:int):
        validator.validate(value, int)
        if value <= 0:
            raise argument_exception("Некорректный аргумент!")
        
        self.__quantity = value
        
    """
    Фабричный метод
    """    
    def create(nomenclature: nomenclature_model, range: range_model, quantity: int):
        validator.validate(quantity, int)
        validator.validate(nomenclature, nomenclature_model)
        validator.validate(range, range_model)

        item =  ingredient_model()
        item.quantity = quantity
        item.nomenclature = nomenclature
        item.range = range
        return item

        
            
    
