from Src.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Core.transation_type import transaction_type
import unittest


"""
Набор тестов для проверки работы старта приложения
"""
class test_start(unittest.TestCase):
    
    """
    Проверить создание инстанса start_service
    """
    def test_create_start_service(self):
        # Подготовка
        reposity = data_reposity()

        # Действие
        start = start_service(reposity)

        # Проверки
        assert start is not None

    """
    Проверить генерацию стартовых элементов системы
    """
    def test_start_service_create(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)

        # Действие
        result = start.create()

        # Проверки
        assert start is not None
        assert result == True
        assert start.is_error == False

    """
    Проверить состав стартовых элементов
    """
    def test_start_service_consists_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        # Действие
        found = list(filter(lambda x: x.name == "грамм", reposity.data[data_reposity.range_key()]  ))

        # Проверки
        assert len(found) == 1


    """
    Проверить состав стартовых элементов
    """
    def test_start_service_consists_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()

        # Действие
        found = list(filter(lambda x: x.name == "Пшеничная мука", reposity.data[data_reposity.nomenclature_key()]  ))

        # Проверки
        assert len(found) == 1    
        assert found[0].range is not None
        assert found[0].group is not None

    """
    Проверить состав стартовых элементов
    """
    def test_create_warehouse(self):
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        
        warehouses = reposity.data[reposity.warehouse_key()]
        assert len(warehouses) > 0, "Склад не был создан"

        assert warehouses[0].address == "test_address_1"
        assert warehouses[1].address == "test_address_2"

    def test_create_transaction(self):
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        
        transactions = reposity.data[reposity.warehouse_transaction_key()]
        assert len(transactions) == 3, "Транзакции не были созданы или их количество неверное"

        transaction = transactions[0]
        assert transaction.warehouse is not None, "Склад у транзакции не установлен"
        assert transaction.nomenclature is not None, "Номенклатура транзакции не установлена"
        assert transaction.quantity > 0, "Количество транзакции должно быть больше 0"
        assert transaction.transaction_type in list(transaction_type), "Неверный тип транзакции"
        assert transaction.range is not None, "Единица измерения транзакции не установлена"
        assert transaction.period is not None, "Период транзакции не установлен"




if __name__ == '__main__':
    unittest.main()