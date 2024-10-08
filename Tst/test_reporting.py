from Src.start_service import start_service
from Src.data_reposity import data_reposity
from Src.Reports.csv_report import csv_report
from Src.Reports.report_factory import report_factory
from Src.Core.format_reporting import format_reporting
from Src.Reports.csv_report import csv_report
from Src.Reports.json_report import json_report
from Src.Reports.xml_report import xml_report
from Src.settings_manager import settings_manager

import unittest


"""
Набор тестов для проверки работы формирование отчетов
"""
class test_reporting(unittest.TestCase):

    """
    Проверить формирование словаря с типами форматов для отчетов
    """
    def test_get_format_reporting(self):
        # Подготовка
 
        # Действие
        result = format_reporting.list()

        # Проверка
        assert result is not None
    
    """
    Проверка работы отчета Xml
    """
    def test_xml_report_create_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = xml_report()

        # Действие
        report.create(reposity.data[ data_reposity.range_key()  ])

        # Проверки
        assert report.result != ""
        with open('test_xml_report_create_range.xml', 'w') as file:
            file.write(report.result)


    """
    Проверка работы отчета Xml
    """
    def test_xml_report_create_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = xml_report()

        # Действие
        report.create(reposity.data[ data_reposity.nomenclature_key()  ])

        # Проверки
        assert report.result != ""
        with open('test_xml_report_create_nomenclature.xml', 'w') as file:
            file.write(report.result)



    """
    Проверка работы отчета Xml
    """
    def test_xml_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = xml_report()

        # Действие
        report.create(reposity.data[ data_reposity.receipt_key()  ])

        # Проверки
        assert report.result != ""
        with open('test_xml_report_create_receipt.xml', 'w') as file:
            file.write(report.result)



    """
    Проверка работы отчета Json
    """
    def test_json_report_create_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = json_report()

        # Действие
        report.create(reposity.data[ data_reposity.range_key()  ])

        # Проверки
        assert report.result != ""
        with open('test_json_report_create_range.json', 'w') as file:
            file.write(report.result)


    """
    Проверка работы отчета Json
    """
    def test_json_report_create_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = json_report()

        # Действие
        report.create(reposity.data[ data_reposity.nomenclature_key()  ])

        # Проверки
        assert report.result != ""
        with open('test_json_report_create_nomenclature.json', 'w') as file:
            file.write(report.result)

    """
    Проверка работы отчета Json
    """
    def test_json_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = json_report()

        # Действие
        report.create(reposity.data[ data_reposity.receipt_key()  ])

        # Проверки
        assert report.result != ""
        with open('test_json_report_create_receipt.json', 'w') as file:
            file.write(report.result)        


    """
    Проверка работы отчета CSV
    """
    def test_csv_report_create_range(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.range_key()  ])

        # Проверки
        assert report.result != ""
        with open('test_csv_report_create_range.csv', 'w') as file:
            file.write(report.result)


    """
    Проверка работы отчета CSV
    """
    def test_csv_report_create_nomenclature(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.nomenclature_key()  ])

        # Проверки
        assert report.result != ""    
        with open('test_csv_report_create_nomenclature.csv', 'w') as file:
            file.write(report.result)


    """
    Проверка работы отчета CSV
    """
    def test_csv_report_create_receipt(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()
        report = csv_report()

        # Действие
        report.create(reposity.data[ data_reposity.receipt_key()  ])

        # Проверки
        assert report.result != ""     
        with open('test_csv_report_create_receipt.csv', 'w') as file:
            file.write(report.result) 



    """
    Проверить работу фабрики для получения инстанса нужного отчета
    """
    def test_report_factory_create_default(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()   
        manager = settings_manager()
        manager.open("../settings.json")

       
        # Действие
        report = report_factory(manager.settings).create_default( )

        # Проверка
        assert report is not None


    """
    Проверить работу фабрики для получения инстанса нужного отчета
    """
    def test_report_factory_create_csv(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()   
        manager = settings_manager()
        manager.open("../settings.json")

       
        # Действие
        report = report_factory(manager.settings).create( format_reporting.CSV )

        # Проверка
        assert report is not None
        assert isinstance(report,  csv_report)


    """
    Проверить работу фабрики для получения инстанса нужного отчета
    """
    def test_report_factory_create_xml(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()   
        manager = settings_manager()
        manager.open("../settings.json")

       
        # Действие
        report = report_factory(manager.settings).create( format_reporting.XML )

        # Проверка
        assert report is not None
        assert isinstance(report,  xml_report)    

    """
    Проверить работу фабрики для получения инстанса нужного отчета
    """
    def test_report_factory_create_json(self):
        # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()   
        manager = settings_manager()
        manager.open("../settings.json")

       
        # Действие
        report = report_factory(manager.settings).create( format_reporting.JSON )

        # Проверка
        assert report is not None
        assert isinstance(report,  json_report)          

    """
    Проверить работу фабрики. Не реализован формат
    """
    def test_report_factory_create_fail(self):
         # Подготовка
        reposity = data_reposity()
        start = start_service(reposity)
        start.create()        
        manager = settings_manager()
        manager.open("../settings.json")
        factory = report_factory(manager.settings)
       
        # Действие
        report = factory.create( format_reporting.MARKDOWN )

        # Проверка
        assert report is None
        assert factory.is_error == True




if __name__ == '__main__':
    unittest.main()           
