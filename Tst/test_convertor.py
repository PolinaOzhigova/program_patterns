import unittest
from Src.data_reposity import data_reposity
from Src.start_service import start_service
from Src.Core.common import common
from Src.Core.convert_factory import convert_factory
from Src.Models.range import range_model
from Src.Models.nomenclature import nomenclature_model
from Src.Models.receipt import receipt_model

"""
Набор тестов для проверки работы  конвертора данных (сериализация / десериализация)
"""
class test_convertor(unittest.TestCase):

    """
    Проверить метод получения списка полей которые имеют ссылочный тип на модель
    """
    def test_common_get_fields_models(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        if len(reposity.data)  <= 0:
            raise Exception("Список данных пуст!")
        
        instance = reposity.data[ data_reposity.range_key()][0]

        # Действие
        fields = common.get_fields_models(instance)

        # Проверки
        assert len(fields) > 0

    """
    Проверить десериализацию простой вложенной модели
    """
    def test_deserialize_range_model(self):
        # Подготовка 
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        if len(reposity.data)  <= 0:
            raise Exception("Набор данных пуст!")
        
        factory = convert_factory()
        data = {
                "base": {
                    "base": None,
                    "name": "грамм",
                    "unique_code": "bbc02124f4bb4678bc4ba45ed89a2c4f",
                    "value": 1
                },
                "name": "кг",
                "unique_code": "0bb36f73b67d400e98aa0d1aaaf18b3a",
                "value": 1000
            }
        result = range_model()
        

        # Действие
        factory.deserialize(data, result)

        # Проверки
        assert result is not None
        assert result.base is not None
        assert result.base.base is None

    """
    Проверить десериализацию простой вложенной модели
    """
    def test_deserialize_nomenclature_model(self):
        # Подготовка 
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        if len(reposity.data)  <= 0:
            raise Exception("Набор данных пуст!")
        
        factory = convert_factory()
        data = {
                "group": {
                    "name": "Сырье",
                    "unique_code": "33e83cf0bd3a453791cde7c5ce5c6168"
                },
                "name": "Пшеничная мука",
                "range": {
                    "base": {
                        "base": None,
                        "name": "грамм",
                        "unique_code": "d6e4d2f149fc433c944a7ff94a61c3b9",
                        "value": 1
                    },
                    "name": "кг",
                    "unique_code": "cf797608c3724ed4861fde88242ca86c",
                    "value": 1000
                },
                "unique_code": "669a6091d5514784a71fc6ff2a262ff7"
            }
        result = nomenclature_model()
        

        # Действие
        factory.deserialize(data, result)

        # Проверки
        assert result is not None
        assert result.range is not None
        assert result.group is not None
        assert result.range.base is not None

    """
    Проверить десериализацию комплексной модели
    """
    def test_deserialize_receipt(self):
        # Подготовка 
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        if len(reposity.data)  <= 0:
            raise Exception("Набор данных пуст!")
        factory = convert_factory()
        receipt = reposity.data[ data_reposity.receipt_key()][0]
        json = factory.serialize(receipt)
        if len(json) == 0:
            raise Exception("Json данные пусты!")
      
        result = receipt_model()

        # Дейсивие
        factory.deserialize(json, result)

        # Проверки
        assert result is not None
        assert len(result.ingredients) > 0
        assert len(result.instructions) > 0



if __name__ == '__main__':
    unittest.main()   
