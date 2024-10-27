from Src.Core.abstract_process import abstract_process
from Src.Core.transation_type import transaction_type
from Src.Core.validator import validator
from Src.Models.warehouse_stock import warehouse_stock
from Src.Models.warehouse_transactions import warehouse_transaction


class turnover_process(abstract_process):
    def execute(self, transactions: list[warehouse_transaction]) -> list[warehouse_stock]:
        result = {}
        for transaction in transactions:
            validator.validate(transaction, warehouse_transaction)
            warehouse = transaction.warehouse
            nomenclature = transaction.nomenclature
            range_unit = transaction.range
            key = (warehouse, nomenclature, range_unit)
            value = transaction.quantity
            if transaction.transaction_type == transaction_type.USE:
                value = -value
            result[key] = result.get(key, 0) + value
        turns = []
        for key, value in result.items():
            turn = warehouse_stock.create(warehouse=key[0], turnover=value, nomenclature=key[1],
                                                 range=key[2])
            turns.append(turn)
        return turns