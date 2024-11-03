from abc import ABC, abstractmethod

from Src.Models.warehouse_transactions import warehouse_transaction
from Src.Models.warehouse_stock import warehouse_stock


class abstract_process(ABC):

    @abstractmethod
    def execute(self, transactions: list[warehouse_transaction]) -> list[warehouse_stock]:
        pass