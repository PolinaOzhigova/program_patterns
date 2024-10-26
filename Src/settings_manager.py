from Src.Models.settings import settings_model, settings_report_handler
from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import argument_exception, operation_exception, validator
from Src.Core.common import common
from Src.Core.convert_factory import convert_factory


import json
import os

"""
Менеджер настроек
"""
class settings_manager(abstract_logic):
    __file_name = "settings.json"
    __settings:settings_model = None


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(settings_manager, cls).__new__(cls)
        return cls.instance 
     

    def __init__(self) -> None:
        if self.__settings is None:
            self.__settings = self.__default_setting() 

    """
    Открыть и загрузить настройки
    """
    def open(self, file_name:str = ""):
        validator.validate(file_name, str)
        
        if file_name != "":
            self.__file_name = file_name

        try:
            current_path_info = os.path.split(__file__)
            current_path = current_path_info[0]
            full_name = f"{current_path}{os.sep}{self.__file_name}"

            if not os.path.exists(full_name):
                self.set_exception(operation_exception(f"Не найден файл настроек {full_name} Default загрузка"))
                self.__settings = self.__default_setting()
            else:    
                stream = open(full_name)
                data = json.load(stream)

                factory = convert_factory()
                factory.deserialize(data,  self.__settings)
            
            return True
        except Exception as ex :
            self.__settings = self.__default_setting()
            self.set_exception(ex)
            return False

    """
    Загруженные настройки
    """
    @property
    def settings(self) -> settings_model:
        return self.__settings
    

    """
    Набор настроек по умолчанию
    """
    def __default_setting(self) -> settings:
        _settings = settings_model()
        _settings.inn = "123456789"
        _settings.organization_name = "Рога и копыта (default)"
        return _settings
    

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)