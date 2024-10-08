from Src.Core.base_models import base_model_code
from Src.Core.convert_factory import convert_factory
from Src.Core.format_reporting import format_reporting
from Src.Core.validator import validator, argument_exception


"""
Настройка связки меджу форматом и типов обработки
"""
class settings_report_handler(base_model_code):
    __type: format_reporting = format_reporting.CSV
    __handler:str = ""


    """
    Тип отчет
    """
    @property
    def type(self) -> format_reporting:
        return self.__type
    
    @type.setter
    def type(self, value:int ):
        validator.validate(value, int)
        try:
            self.__type = format_reporting(value)
        except:
            raise argument_exception(f"Невозможно преобразовать значение {value} в тип format_reporting!")

    @property
    def handler(self) -> str:
        return self.__handler
    
    @handler.setter
    def handler(self, value: str):
        validator.validate(value, str)
        self.__handler = value


"""
Настройки
"""
class settings_model(base_model_code):
    __organization_name = ""
    __inn = ""
    __default_report_format:format_reporting = format_reporting.CSV
    __report_handlers:list[settings_report_handler] = []

    """
    Наименование организации
    """
    @property
    def organization_name(self):
        return self.__organization_name
    

    @organization_name.setter
    def organization_name(self, value:str):
        validator.validate(value, str, 255)
        self.__organization_name = value

    """
    ИНН
    """
    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, value:str):
        validator.validate(value, str, 9)
        self.__inn = value


    """
    По умолчанию формат
    """
    @property
    def default_report_format(self) -> format_reporting:
        return self.__default_report_format
    
    @default_report_format.setter
    def default_report_format(self, value:int):
        validator.validate(value, int)
        try:
            self.__default_report_format = format_reporting(value)
        except:
            raise argument_exception(f"Невозможно преобразовать значение {value} в тип format_reporting!")


    """
    Набор обработчиков для
    """
    @property
    def report_handlers(self) -> list[settings_report_handler]:
        return self.__report_handlers

    @report_handlers.setter
    def report_handlers(self, value:list ):
        validator.validate(value, list)
        self.__report_handlers = value

    """
    Дополнительный метод для десериализации
    """
    def deserialize(self, data:dict ):   
        super().deserialize(data)

        if "report_handlers" in data.keys():
            # Набор комментариев
            self.report_handlers.clear()
            factory = convert_factory()
            source = data["report_handlers"]   
            for item in source:
                instance = settings_report_handler()
                factory.deserialize(item, instance)
                self.report_handlers.append(instance)
    





