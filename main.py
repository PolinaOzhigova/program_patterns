import re
import connexion
from Src.Core.format_reporting import format_reporting
from Src.Reports import report_factory
from Src.Core.validator import operation_exception, validator
from Src.data_reposity import data_reposity
from Src.settings_manager import settings_manager
from Src.start_service import start_service
from Src.Reports.report_factory import report_factory



app = connexion.FlaskApp(__name__)

reposity = data_reposity()
start = start_service(reposity)
start.create()

manager = settings_manager()
manager.open("settings.json")
factory = report_factory(manager.settings)

"""
Получить список форматов отчетов
"""
@app.route("/api/reports/formats", methods=['GET'])
def formats():
    return format_reporting.list()

"""
Получить список сущностей
"""
@app.route("/api/reports/entities", methods=['GET'])
def entities():
    return data_reposity.keys()


"""
Получить отчет по списоку единиц измерения
Источник: https://github.com/Danila-Ivashchenko
"""
@app.route("/app/reports/<entity>/<format>", methods=["GET"])
def get_report(entity:str, format:int):
    validator.validate(format, int)
    validator.validate(entity, str)
    if not format_reporting.check(format):
        raise operation_exception("Некорректно указан формат отчета! См метод /api/report/formats")
    
    if entity not in data_reposity.keys():
        raise operation_exception("Некорректно указан тип данных! См метод /api/report/entities")

    report_format = format_reporting(format)
    report = factory.create(report_format)

    if report is None:
        raise operation_exception("Невозможно подобрать корректный отчет согласно параметрам!")
    
    if len(reposity.data) == 0:
        raise operation_exception("Набор данных пуст!")

    result = report.create(reposity.data[ entity ])
    if result == False:
        raise operation_exception(report.error_text)
    
    return report.result
    


if __name__ == '__main__':
    app.add_api('swagger.yaml' )
    app.run(port = 8080)

