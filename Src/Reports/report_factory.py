from Src.Core.abstract_logic import abstract_logic
from Src.Core.abstract_report import abstract_report
from Src.Core.format_reporting import format_reporting
from Src.Reports.json_report import json_report
from Src.Reports.xml_report import xml_report
from Src.Reports.csv_report import csv_report
from Src.Core.validator import validator, operation_exception
from Src.Models.settings import settings_model, settings_report_handler


"""
Фабрика для формирования отчетов
"""
class report_factory(abstract_logic):
    __reports = {}
    __settings: settings_model = None

    def __init__(self, settings: settings_model) -> None:
        super().__init__()
        validator.validate(settings, settings_model)
        self.__settings = settings
        self.__build_mapping()


    """
    Получить инстанс нужного отчета
    """
    def create(self, format: format_reporting) ->  abstract_report: 
        validator.validate(format, format_reporting)
        
        if format not in self.__reports.keys() :
            self.set_exception( operation_exception(f"Указанный вариант формата {format} не реализован!"))
            return None
        
        report = self.__reports[format]
        return report()
    

    """
    Получить инстанс отчета default формата
    """
    def create_default(self) -> abstract_report:
        format = self.__settings.default_report_format
        return self.create(format)

    """
    Сформировать набор связей из настроек
    """
    def __build_mapping(self):
        if self.__settings is None:
            raise operation_exception("Настройки некорректны!")
        
        self.__reports.clear()

        if len(self.__settings.report_handlers) == 0:
            # Default схема
            
            self.__reports[ format_reporting.CSV ] = csv_report
            self.__reports[ format_reporting.JSON ] = json_report
            self.__reports[ format_reporting.XML ] = xml_report
            return
        
        for item in self.__settings.report_handlers:
            if item.type not in self.__reports.keys():
                try:
                    self.__reports[item.type] = eval(item.handler)
                except:
                    raise operation_exception("Некорректные настройки!")

    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)
       



    
