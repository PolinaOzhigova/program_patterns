import unittest
from datetime import datetime, timedelta
from Src.Core.validator import validator
from Src.Observe_objects.observe_osb import observe_osb
from Src.Models.warehouse_transactions import warehouse_transaction
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity

class MockWarehouse:
    def __init__(self, address):
        self.address = address

class MockTransactionType:
    OSB = "OSB"

class MockDataRepository:
    data = {}

    @staticmethod
    def osb_key():
        return "osb_key"

class MockWarehouseTransaction(warehouse_transaction):
    def __init__(self, warehouse, period):
        self.__warehouse = warehouse
        self.__period = period

    @property
    def warehouse(self):
        return self.__warehouse

    @property
    def period(self):
        return self.__period


class ObserveOSBTest(unittest.TestCase):
    def setUp(self):
        self.observer = observe_osb()
        self.observer.reposity = MockDataRepository

    def test_single_transaction(self):
        warehouse = MockWarehouse(address="Address1")
        transaction = MockWarehouseTransaction(warehouse=warehouse, period=datetime(2024, 10, 26))

        result = self.observer.handle_event(type=event_type.OSB, params=[transaction])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], datetime(2024, 10, 26))
        self.assertIsNone(result[0][1])
        self.assertEqual(result[0][2], warehouse) 
        self.assertEqual(result[0][3], transaction)

    def test_multiple_transactions_same_address(self):
        warehouse = MockWarehouse(address="Address1")
        transaction1 = MockWarehouseTransaction(warehouse=warehouse, period=datetime(2024, 10, 25))
        transaction2 = MockWarehouseTransaction(warehouse=warehouse, period=datetime(2024, 10, 26))

        result = self.observer.handle_event(type=event_type.OSB, params=[transaction1, transaction2])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], datetime(2024, 10, 26))
        self.assertEqual(result[0][1], datetime(2024, 10, 25))
        self.assertEqual(result[0][2], warehouse)
        self.assertEqual(result[0][3], transaction2)

    def test_multiple_transactions_different_addresses(self):
        warehouse1 = MockWarehouse(address="Address1")
        warehouse2 = MockWarehouse(address="Address2")
        transaction1 = MockWarehouseTransaction(warehouse=warehouse1, period=datetime(2024, 10, 25))
        transaction2 = MockWarehouseTransaction(warehouse=warehouse2, period=datetime(2024, 10, 26))

        result = self.observer.handle_event(type=event_type.OSB, params=[transaction1, transaction2])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], datetime(2024, 10, 25))
        self.assertIsNone(result[0][1])
        self.assertEqual(result[0][2], warehouse1)
        self.assertEqual(result[0][3], transaction1)

        self.assertEqual(result[1][0], datetime(2024, 10, 26))
        self.assertIsNone(result[1][1])
        self.assertEqual(result[1][2], warehouse2)
        self.assertEqual(result[1][3], transaction2)

    def test_transaction_updates_repository(self):
        warehouse = MockWarehouse(address="Address1")
        transaction = MockWarehouseTransaction(warehouse=warehouse, period=datetime(2024, 10, 26))

        self.observer.handle_event(type=event_type.OSB, params=[transaction])

        repo_data = self.observer.reposity.data.get(MockDataRepository.osb_key())
        self.assertIsNotNone(repo_data)
        self.assertEqual(len(repo_data), 1)
        self.assertEqual(repo_data[0][0], datetime(2024, 10, 26))
        self.assertIsNone(repo_data[0][1])
        self.assertEqual(repo_data[0][2], warehouse)
        self.assertEqual(repo_data[0][3], transaction)

if __name__ == "__main__":
    unittest.main()
