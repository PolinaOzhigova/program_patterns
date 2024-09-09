from modules.settings import Settings
import json
import os

class Settings_manager:
    __file_name = "settings.json"
    __settings: Settings = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Settings_manager, cls).__new__(cls)
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
            else:
                print(f"Поле '{field}' отсутствует в данных. Изменен на None.")
                setattr(self.__settings, field, None)

    @property
    def settings(self):
        return self.__settings

    def __default_setting(self):
        data = Settings()
        data.inn = "0" * 12
        data.organization_name = "DEFAULT_ORG_NAME"
        data.bank_account = "0" * 11
        data.correspondent_account = "0" * 11
        data.type_property = "0" * 5
        data.bik = "0" * 9

        return data
