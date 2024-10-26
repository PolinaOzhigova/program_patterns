from Src.Core.base_models import  base_model_name
from Src.Core.validator import validator
from Src.Models.warehouse import warehouse
from Src.Models.nomenclature import nomenclature_model
from Src.Models.range import range_model

class warehouse_stock(base_model_name):
    __warehouse: warehouse
    __turnover: float = 0.0
    __nomenclature: nomenclature_model
    __range: range_model

    @property
    def warehouse(self) -> warehouse:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse):
        validator.validate(value, warehouse)
        self.__warehouse = value

    @property
    def turnover(self) -> float:
        return self.__turnover

    @turnover.setter
    def turnover(self, value: float):
        validator.validate(value, float)
        self.__turnover = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    @staticmethod
    def create(
            warehouse:warehouse=None,
            nomenclature: nomenclature_model=None,
            range: range_model = None,
            turnover: int = 0
    ):

        item = warehouse_stock()

        item.warehouse = warehouse
        item.nomenclature = nomenclature
        item.range = range
        item.turnover = turnover

        return item