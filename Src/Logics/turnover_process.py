from Src.Core.abstract_process import abstract_process
from Src.Core.transation_type import transaction_type
from Src.Core.validator import validator
from Src.Models.warehouse_stock import warehouse_stock
from Src.Models.warehouse_transactions import warehouse_transaction
from Src.data_reposity import data_reposity
from datetime import datetime
from Src.settings_manager import settings_manager

class turnover_process(abstract_process):
    reposity = data_reposity()

    def execute(self, transactions: list[warehouse_transaction]) -> list[warehouse_stock]:
        manager = settings_manager()

        turns1 = None
        if "turnover_process_key" in self.reposity.data.keys():
            turns1 = self.reposity.data[data_reposity.turnover_process_key()]
            date_start = [manager.settings.data_block]
            date_end = datetime.now()
        else: 
            date_start = datetime(1900,1,1)
            date_end = manager.settings.data_block
        result = {}
        for transaction in transactions:
            validator.validate(transaction, warehouse_transaction)
            warehouse = transaction.warehouse
            if transaction.period < date_start or transaction.period > date_end:
                continue

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

        self.reposity.data[data_reposity.turnover_process_key()] = turns
        if turns1 != None:
            turns.extend(turns1)
        return turns
    