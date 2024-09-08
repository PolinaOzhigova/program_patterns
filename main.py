import json
import os
import unittest

class settings:
    __organization_name = ""
    __inn = ""
    __bank_account = ""
    __correspondent_account = ""
    __bik = ""
    __type_property = ""

    @property
    def organization_name(self):
        return self.__organization_name
    
    @organization_name.setter
    def organization_name(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Некорректно передан параметр!")
        self.__organization_name = value

    @property
    def inn(self):
        return self.__inn
    
    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str) or len(value) != 12:
            raise TypeError("Длина ИНН должна быть 12 символов!")
        self.__inn = value

    @property
    def bank_account(self):
        return self.__bank_account
    
    @bank_account.setter
    def bank_account(self, value: str):
        if not isinstance(value, str) or len(value) != 11:
            raise TypeError("Длина счета должна быть 11 символов!")
        self.__bank_account = value

    @property
    def correspondent_account(self):
        return self.__correspondent_account
    
    @correspondent_account.setter
    def correspondent_account(self, value: str):
        if not isinstance(value, str) or len(value) != 11:
            raise TypeError("Длина корреспондентского счета должна быть 11 символов!")
        self.__correspondent_account = value

    @property
    def bik(self):
        return self.__bik
    
    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str) or len(value) != 9:
            raise TypeError("Длина БИК должна быть 9 символов!")
        self.__bik = value

    @property
    def type_property(self):
        return self.__type_property
    
    @type_property.setter
    def type_property(self, value: str):
        if not isinstance(value, str) or len(value) != 5:
            raise TypeError("Длина типа собственности должна быть 5 символов!")
        self.__type_property = value


class settings_manager:
    __file_name = "settings.json"
    __settings: settings = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance
    
    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting()

    def open(self, file_name: str = ""):
        if not isinstance(file_name, str):
            raise TypeError("Некорректно переданы параметры!")
        
        if file_name != "":
            self.__file_name = file_name
        
        try:
            full_name = os.path.abspath(self.__file_name)
            with open(full_name, 'r') as stream:
                data = json.load(stream)
                self.convert(data)

            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.__settings = self.__default_setting()
            return False

    def convert(self, data: dict):
        fields = list(filter(lambda x: not x.startswith("_"), dir(self.__settings.__class__)))

        for field in fields:
            if field in data:
                value = data[field]
                setattr(self.__settings, field, value)

    @property
    def settings(self):
        return self.__settings

    def __default_setting(self):
        data = settings()
        data.inn = "0" * 12
        data.organization_name = "DEFAULT_ORG_NAME"
        data.bank_account = "0" * 11
        data.correspondent_account = "0" * 11
        data.type_property = "0" * 5
        data.bik = "0" * 9

        return data

class TestSettingsManager(unittest.TestCase):

    def setUp(self):
        self.manager = settings_manager()

        self.test_data = {
            "organization_name": "Test Organization",
            "inn": "123456789012",
            "bank_account": "12345678901",
            "correspondent_account": "10987654321",
            "bik": "123456789",
            "type_property": "AB123"
        }

        # Создание тестового файла
        self.test_file_name = "test_settings.json"
        with open(self.test_file_name, 'w') as f:
            json.dump(self.test_data, f)

        # Создание тестового файла в другом каталоге
        self.test_file_dir = os.path.join(os.getcwd(), "test_dir")
        os.makedirs(self.test_file_dir, exist_ok=True)
        self.test_file_path = os.path.join(self.test_file_dir, "other_settings.json")
        with open(self.test_file_path, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        # Удаление тестовых файлов
        os.remove(self.test_file_name)
        os.remove(self.test_file_path)
        os.rmdir(self.test_file_dir)

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


if __name__ == "__main__":
    unittest.main()