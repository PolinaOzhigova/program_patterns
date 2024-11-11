from Src.data_reposity import data_reposity
from Src.start_service import start_service
from Src.settings_manager import settings_manager
from Src.Logics.observe_service import observe_service
from Src.Core.event_type import event_type
from Src.start_service import start_service
from Src.Models.nomenclature import nomenclature_model
from Src.Logics.nomenclature_service import nomenclature_service

import unittest
from copy import copy

class test_monenclature_service(unittest.TestCase):
    # Подготовка
    manager = settings_manager()
    manager.open("../settings.json")
    reposity = data_reposity()
    start = start_service(reposity)
    start.create()

    
    def test_get(self):
        items = self.reposity.data[data_reposity.nomenclature_key()]
        items: list[nomenclature_model]

        service = nomenclature_service(self.reposity)
        service.data_reposity = self.reposity

        for i in range(len(items)):
            self.assertEqual(items[i], service.get( items[i].unique_code))

        self.assertNotEqual(items[1],service.get(items[0].unique_code))

    def test_put(self):
        items = self.reposity.data[data_reposity.nomenclature_key()]
        items: list[nomenclature_model]

        service = nomenclature_service(self.reposity)
        service.data_reposity = self.reposity

        new_item = items[1].copy()

        service.put(new_item)

        self.assertEqual(items[-1],new_item)


    def test_delete_item(self):
        items = self.reposity.data[data_reposity.nomenclature_key()]
        items: list[nomenclature_model]

        service = nomenclature_service(self.reposity)
        service.data_reposity = self.reposity

        delete_item = items[0]

        status = service.delete(delete_item.unique_code)

        self.assertEqual(status,True)

        for i in items:
            self.assertNotEqual(i,delete_item)