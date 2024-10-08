import unittest

from Src.Dto.filter import Filter
from Src.Logics.nomenclature_prototype import NomenclaturePrototype
from Src.data_reposity import data_reposity
from Src.start_service import start_service
from main import reposity


class TestPrototype(unittest.TestCase):

    def test_prototype_nomenclature(self):
        repository = data_reposity()
        start = start_service(reposity)
        start.create()
        if len(repository.data[data_reposity.nomenclature_key()]) == 0:
            raise Exception("No data")
        data = repository.data[data_reposity.nomenclature_key()]
        item = data[0]
        item_filter = Filter()
        item_filter.name = item.name

        prototype = NomenclaturePrototype(data)
        prototype.create(data, item_filter)
        assert len(prototype.data) == 1
        assert prototype.data[0] == item
