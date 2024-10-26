from Src.Core.base_models import  base_model_name
from Src.Core.validator import validator

class warehouse(base_model_name):
    __address: str = ""

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, value: str):
        validator.validate(value, str)
        self.__address = value

    @staticmethod
    def create(
            name="test_warehouse",
            address="test_address"
    ):
        item_warehouse = warehouse()
        item_warehouse.address = address
        return item_warehouse