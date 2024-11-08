from Src.Models.settings import settings_model, settings_report_handler
from Src.Core.abstract_logic import abstract_logic
from Src.Core.validator import argument_exception, operation_exception, validator
from Src.Core.common import common
from Src.Core.convert_factory import convert_factory
from Src.Core.event_type import event_type
# from Src.Logics.observe_service import observe_service
from datetime import datetime
from Src.Models.settings import settings_report_handler
from Src.Core.format_reporting import format_reporting


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

        # observe_service.append(self)


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
    Сохранить настройки
    """
    def save(self, file_name:str = ""):
        validator.validate(file_name, str)
        
        if file_name != "":
            self.__file_name = file_name

        try:
            current_path_info = os.path.split(__file__)
            current_path = current_path_info[0]
            full_name = f"{current_path}{os.sep}{self.__file_name}"

            if os.path.exists(full_name):
                os.remove(full_name)

            # Готовим Json
            factory = convert_factory()
            items = factory.serialize(self.__settings)    
            result = json.dumps(items, ensure_ascii=False, indent=4)

            # Записываем в файл
            with open(full_name, "w") as file:
                file.write(result)
            
            return True
        except Exception as ex :
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
        default_settings = settings_model()
        default_settings.inn = "123456789"
        default_settings.organization_name = "Рога и копыта (default)"
        default_settings.data_block = datetime.now()
        default_settings.default_report_format = format_reporting.JSON.value

        handlers = []
        handlers.append(  settings_report_handler.create( format_reporting.CSV.value, "csv_report" ) )
        handlers.append(  settings_report_handler.create( format_reporting.XML.value, "xml_report" ) )
        handlers.append(  settings_report_handler.create( format_reporting.JSON.value, "json_report" ) )
        default_settings.report_handlers = handlers

        return default_settings
    

    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)

    def handle_event(self, type: event_type, params ):
        super().handle_event(type, params)       

        if type == event_type.CHANGE_BLOCK_PERIOD:
            self.save(self.__file_name)