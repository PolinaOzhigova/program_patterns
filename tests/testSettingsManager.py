from modules.settings_manager import Settings_manager
import unittest
import json
import os

class TestSettingsManager(unittest.TestCase):

    def setUp(self):
        self.manager = Settings_manager()

        self.test_data = {
            "organization_name": "Test Organization",
            "inn": "123456789012",
            "bank_account": "12345678901",
            "correspondent_account": "10987654321",
            "bik": "123456789",
            "type_property": "AB123"
        }

        self.test_file_name = "test_settings.json"
        with open(self.test_file_name, 'w') as f:
            json.dump(self.test_data, f)

        self.test_file_dir = os.path.join(os.getcwd(), "test_dir")
        os.makedirs(self.test_file_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_file_dir, "other_settings.json")
        with open(self.test_file_path, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        os.remove(self.test_file_name)
        os.remove(self.test_file_path)
        os.rmdir(self.test_file_dir)

    def test_singleton_enabled(self):
        """
        Проверка включенного Singleton паттерна
        """
        manager1 = Settings_manager()
        manager2 = Settings_manager()

        self.assertIs(manager1, manager2, "Singleton нарушен: объекты manager1 и manager2 разные!")

    def test_singleton_disabled(self):
        """
        Проверка отключенного Singleton паттерна.
        """
        original_new = Settings_manager.__new__

        def mock_new(cls, *args, **kwargs):
            return super(Settings_manager, cls).__new__(cls)

        try:
            Settings_manager.__new__ = mock_new

            manager1 = Settings_manager()
            manager2 = Settings_manager()

            self.assertIsNot(manager1, manager2, "Singleton не отключен: объекты manager1 и manager2 одинаковы!")
        
        finally:
            Settings_manager.__new__ = original_new

    def test_load_settings(self):
        self.manager.open(self.test_file_name)
        settings = self.manager.settings

        self.assertEqual(settings.organization_name, self.test_data["organization_name"])
        self.assertEqual(settings.inn, self.test_data["inn"])
        self.assertEqual(settings.bank_account, self.test_data["bank_account"])
        self.assertEqual(settings.correspondent_account, self.test_data["correspondent_account"])
        self.assertEqual(settings.bik, self.test_data["bik"])
        self.assertEqual(settings.type_property, self.test_data["type_property"])

    def test_load_settings_from_different_dir(self):
        self.manager.open(self.test_file_path)
        settings = self.manager.settings

        self.assertEqual(settings.organization_name, self.test_data["organization_name"])
        self.assertEqual(settings.inn, self.test_data["inn"])
        self.assertEqual(settings.bank_account, self.test_data["bank_account"])
        self.assertEqual(settings.correspondent_account, self.test_data["correspondent_account"])
        self.assertEqual(settings.bik, self.test_data["bik"])
        self.assertEqual(settings.type_property, self.test_data["type_property"])
