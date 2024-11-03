import unittest
from datetime import datetime
from Src.data_reposity import data_reposity
from Src.start_service import start_service
from Src.Core.transation_type import transaction_type
from Src.Models.warehouse import warehouse
from Src.Models.warehouse_transactions import warehouse_transaction
from Src.Models.warehouse_stock import warehouse_stock
from Src.Logics.turnover_process import turnover_process
from datetime import datetime
from Src.settings_manager import settings_manager


class test_processes(unittest.TestCase):
    def test_turnover_both_process(self):
        """
        Тест оборота по приходу и расходу
        """
        # Подготовка
        manager1 = settings_manager()
        manager1.open("../settings.json")
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        warehouse = reposity.data[reposity.warehouse_key()][0]
        nomenclature = reposity.data[reposity.nomenclature_key()][0]
        range_unit = reposity.data[reposity.range_key()][0]
        transaction1 = warehouse_transaction.create(
            warehouse=warehouse, nomenclature=nomenclature, quantity=30.0, range=range_unit, transaction_type=transaction_type.COME, period=datetime.now()
        )
        transaction2 = warehouse_transaction.create(
            warehouse=warehouse, nomenclature=nomenclature, quantity=10.0, range=range_unit, transaction_type=transaction_type.USE, period=datetime.now()
        )
        transactions = [transaction1, transaction2]
        process = turnover_process()
        turns = process.execute(transactions)
        assert len(turns) == 1
        assert turns[0].turnover == 20.0

if __name__ == '__main__':
    unittest.main()