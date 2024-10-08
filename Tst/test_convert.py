from Src.Core.convert_factory import convert_factory
from Src.data_reposity import data_reposity
from Src.Core.validator import operation_exception
from Src.start_service import start_service
import unittest


"""
Набор тестов для проверки работы конвертора объекта в словарь
"""
class test_convert(unittest.TestCase):

    """
    Проверить конвертацию номенклатуры в словарь
    """
    def test_convert_nomenclature(self):
        # Подготовка
        factory = convert_factory()
        storage = data_reposity()
        start = start_service(storage)
        start.create()
        items = storage.data[ data_reposity.nomenclature_key() ]
        if len(items) == 0:
            raise operation_exception("Нет данных для модульного теста!")
        item = items[0]

        # Действие
        result = factory.serialize(item)

        # Проверки
        assert isinstance(result, dict)
        # Количество полей = количеству ключей
        assert len(result) == 4

    """
    Тест конвертации рецепта в словарь
    """
    def test_convert_receipt(self):
        # Подготовка
        factory = convert_factory()
        storage = data_reposity()
        start = start_service(storage)
        start.create()
        items = storage.data[ data_reposity.receipt_key() ]
        if len(items) == 0:
            raise operation_exception("Нет данных для модульного теста!")
        item = items[0]

        # Действие
        result = factory.serialize(item)

        # Проверки
        assert isinstance(result, dict)
        # Количество полей = количеству ключей
        assert len(result) == 6






    


if __name__ == '__main__':
    unittest.main()       