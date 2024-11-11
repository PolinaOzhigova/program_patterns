from Src.data_reposity import data_reposity
from Src.start_service import start_service
from Src.settings_manager import settings_manager
from Src.Logics.observe_service import observe_service
from Src.Core.event_type import event_type
import unittest

class test_observe_service(unittest.TestCase):
    # Подготовка
    manager = settings_manager()
    manager.open("../settings.json")
    reposity = data_reposity()
    start = start_service(reposity)
    start.create()


    def test_update(self):

        observer = observe_service()
        observer.data_reposity = self.reposity

        list_nomenclature = self.reposity.data[data_reposity.nomenclature_key()]

        self.assertEqual(observer.raise_event( event_type.CHANGE_NOMENCLATURE, list_nomenclature ), True)