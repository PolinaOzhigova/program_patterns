from Src.Core.abstract_process import abstract_process
from Src.Core.transation_type import transaction_type
from Src.Core.validator import validator
from Src.Models.warehouse_stock import warehouse_stock
from Src.Models.warehouse_transactions import warehouse_transaction
from Src.Models.settings import settings_model
from Src.data_reposity import data_reposity
from datetime import datetime
from Src.settings_manager import settings_manager

class turnover_process(abstract_process):
    def execute(self, transactions: list[warehouse_transaction]) -> list[warehouse_stock]:
        manager = settings_manager()
        reposity = data_reposity()
        turns1 = 0
        if reposity.data[reposity.turnover_process_key()] != None:
            turns1 = reposity.data[reposity.turnover_process_key()]
            date_start = [reposity.data_block_key()]
            date_end = datetime.now().strftime("%Y-%m-%d")
        else: 
            date_start = datetime(1900,1,1)
            date_end = manager.settings.data_block
        result = {}
        for transaction in transactions:
            validator.validate(transaction, warehouse_transaction)
            warehouse = transaction.warehouse
            if warehouse_transaction.period < date_start or warehouse_transaction.period > date_end:
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

        reposity.data[reposity.data_block_key()] = date_end
        reposity.data[reposity.turnover_process_key()] = turns
        if turns1 == 0:
            return self.execute(transactions)
        return (turns+turns1)