from Src.Core.base_models import  base_model_name
from Src.Core.validator import validator
from Src.Core.transation_type import transaction_type
from Src.Models.warehouse import warehouse
from Src.Models.nomenclature import nomenclature_model
from Src.Models.range import range_model

from datetime import datetime

class warehouse_transaction(base_model_name):
    __warehouse: warehouse
    __nomenclature: nomenclature_model
    __quantity: float = 0.0
    __transaction_type: transaction_type
    __range: range_model
    __period: datetime

    @property
    def warehouse(self) -> warehouse:
        return self.__warehouse

    @warehouse.setter
    def warehouse(self, value: warehouse):
        validator.validate(value, warehouse)
        self.__warehouse = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        # validator
        self.__quantity = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    @property
    def period(self) -> datetime:
        return self.__period

    @period.setter
    def period(self, value: datetime):
        validator.validate(value, datetime)
        self.__period = value

    @property
    def transaction_type(self) -> transaction_type:
        return self.__transaction_type

    @transaction_type.setter
    def transaction_type(self, value: transaction_type):
        validator.validate(value, transaction_type)
        self.__transaction_type = value

    @staticmethod
    def create(
            warehouse=warehouse,
            nomenclature=nomenclature_model(),
            quantity=1,
            transaction_type=transaction_type,
            range=range_model,
            period=datetime.now()
    ):
        item_warehouse_transaction = warehouse_transaction()

        item_warehouse_transaction.warehouse = warehouse
        item_warehouse_transaction.nomenclature = nomenclature
        item_warehouse_transaction.quantity = quantity
        item_warehouse_transaction.transaction_type = transaction_type
        item_warehouse_transaction.range = range
        item_warehouse_transaction.period = period

        return item_warehouse_transaction
