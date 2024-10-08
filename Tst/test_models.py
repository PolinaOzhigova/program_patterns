                                                                        
import unittest
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model

"""
Набор тестов для проверки работы моделей
"""
class test_models(unittest.TestCase):

    """
    Проверить вариант сравнения (по коду)
    """
    def test_nomenclature_model(self):
        # Подготовка
        item1 = nomenclature_model()
        item1.name = "test1"

        item2 = nomenclature_model()
        item2.name = "test1"

        # Проверка
        assert item1 != item2


    """
    Проверить вариант сравнения (по наименованию)
    """
    def test_range_model(self):
        # Подготовка
        item1 = range_model()
        item1.name = "test1"

        item2 = range_model()
        item2.name = "test1"

        # Проверка
        assert item1 == item2



if __name__ == '__main__':
    unittest.main()       