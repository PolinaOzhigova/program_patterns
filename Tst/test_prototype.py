                                                                        
import unittest
from Src.Core.convert_factory import convert_factory
from Src.Logics.filter_prototype import filter_prototype
from Src.data_reposity import data_reposity
from Src.start_service import start_service
from Src.Core.condition_type import condition_type
from Src.Dto.filter import filter
from Src.Logics.filter_service import filter_service

"""
Набор тестов для проверки прототипов
"""
class test_prototype(unittest.TestCase):

    """
    Проверить работу прототипа. Жесткое сравнение. Номенклатура.
    """
    def test_prototype_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        data = reposity.data[ data_reposity.nomenclature_key()  ]
        if len( data ) == 0:
            raise Exception("Нет данных!")
        item = data[0]
        prototype = filter_prototype(  data )


        # Действие
        result = prototype.create("name", condition_type.EQUALS, item.name)

        # Проверка
        assert len(result.data) == 1
        assert result.data[0] == item

    """
    Проверить работу прототипа. Жесткое сравнение. Единицы измерения.
    """
    def test_prototype_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        data = reposity.data[ data_reposity.range_key()  ]
        if len( data ) == 0:
            raise Exception("Нет данных!")
        prototype = filter_prototype(  data )


        # Действие
        result = prototype.create("name", condition_type.EQUALS, "кг")

        # Проверка
        assert len(result.data) == 1

    """
    Проверить работу прототипа. Жесткое сравнение. Единицы измерения. Вложенность.
    """
    def test_prototype_range_gramm(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        
        if len( reposity.data[ data_reposity.range_key()]) == 0:
            raise Exception("Нет данных!")
        
        data = reposity.data[ data_reposity.range_key()  ]
        prototype = filter_prototype(  data )


        # Действие
        result = prototype.create("name", condition_type.EQUALS, "грамм")

        # Проверка (от грамма и от киллограмма)
        assert len(result.data) == 2    

    """
    Проверить работу прототипа. Жесткое сравнение. Номенклатура.
    """
    def test_prototype_nomenclature_like(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        data = reposity.data[ data_reposity.nomenclature_key()  ]
        if len( data ) == 0:
            raise Exception("Нет данных!")
        prototype = filter_prototype(  data )


        # Действие
        result = prototype.create("name", condition_type.LIKE, "м")

        # Проверка
        assert len(result.data) == 2

    """
    Проверить работу сервиса фильтрации
    """
    def test_filter_service(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        data = reposity.data[ data_reposity.nomenclature_key()  ]
        
        if len( data ) == 0:
            raise Exception("Нет данных!")
        
        service = filter_service()
        filterDto = filter.create_example()

        # Действие
        result = service.filter(data, filterDto)

        # Проверки
        assert len(result) == 1

    """
    Проверить десериализацию Json в модель фильтрации
    """
    def test_filter_deserialize(self):
        # Подготовка
        data = {
            "items": [
                {
                "field": "name",
                "condition": 2,
                "value": "м"
                },
                {
                "field": "name",
                "condition": 1,
                "value": "мука"
                }
            ]}
                    
        factory = convert_factory()
        filterDto = filter()
        
        # Действие
        factory.deserialize(data, filterDto)

        # Проверки
        assert len(filterDto.items) == 2

        
        

        






