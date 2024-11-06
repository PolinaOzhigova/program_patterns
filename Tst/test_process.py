import unittest
from datetime import datetime, timedelta
from Src.data_reposity import data_reposity
from Src.start_service import start_service
from Src.Core.transation_type import transaction_type
from Src.Models.warehouse_transactions import warehouse_transaction
from Src.Logics.turnover_process import turnover_process
from datetime import datetime
from Src.settings_manager import settings_manager
import time


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
        assert turns[0].turnover == 20.0

class test_processes_load(unittest.TestCase):
    def test_turnover_performance(self):
        # Подготовка
        manager1 = settings_manager()
        manager1.open("../settings.json")
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        warehouse = reposity.data[reposity.warehouse_key()][0]
        nomenclature = reposity.data[reposity.nomenclature_key()][0]
        range_unit = reposity.data[reposity.range_key()][0]

        # Генерация транзакций
        transactions = []
        for i in range(1000):
            transaction_type_val = transaction_type.COME if i % 2 == 0 else transaction_type.USE
            quantity = 30.0 if transaction_type_val == transaction_type.COME else 10.0
            transaction = warehouse_transaction.create(
                warehouse=warehouse, 
                nomenclature=nomenclature, 
                quantity=quantity, 
                range=range_unit, 
                transaction_type=transaction_type_val, 
                period=datetime.now() - timedelta(days=i)
            )
            transactions.append(transaction)
        
        # Варианты блокировки
        lock_dates = [datetime.now() - timedelta(days=d) for d in [1, 7, 30, 90, 180, 365]]

        # Запись результатов
        with open("performance_results.md", "w") as f:
            f.write("# Performance Test Results\n")
            f.write("| Lock Date | Calculation Time (seconds) |\n")
            f.write("|-----------|---------------------------|\n")

            for lock_date in lock_dates:
                start_time = time.time()
                
                # Выполнение процесса оборота
                process = turnover_process()
                process.lock_date = lock_date  # Установка даты блокировки
                process.execute(transactions)
                
                # Замер времени
                elapsed_time = time.time() - start_time
                f.write(f"| {lock_date.strftime('%Y-%m-%d')} | {elapsed_time:.4f} |\n")

if __name__ == '__main__':
    unittest.main()