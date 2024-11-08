import connexion
from flask import request
from Src.Core.convert_factory import convert_factory
from Src.Core.format_reporting import format_reporting
from Src.Logics.filter_service import filter_service
from Src.Reports import report_factory
from Src.Core.validator import operation_exception, validator
from Src.data_reposity import data_reposity
from Src.settings_manager import settings_manager
from Src.start_service import start_service
from Src.Reports.report_factory import report_factory
from Src.Dto.filter import filter
from Src.Core.condition_type import condition_type
from datetime import datetime
from Src.Models.settings import settings_model

app = connexion.FlaskApp(__name__)

reposity = data_reposity()
start = start_service(reposity)
start.create()

manager = settings_manager()
manager.open("../settings.json")
factory = report_factory(manager.settings)

"""
Получить список форматов отчетов
"""
@app.route("/api/dictionary/formats", methods=['GET'])
def formats():
    return format_reporting.list()

"""
Получить список сущностей
"""
@app.route("/api/dictionary/entities", methods=['GET'])
def entities():
    return data_reposity.keys()

@app.route("/app/dictionary/conditions", methods=["GET"])
def conditions():
    return condition_type.list()
    

"""
Получить отчет
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

    report.create(reposity.data[ entity ])
    return report.result
    
"""
Получить отчет с учетом фильтрации
"""    
@app.route("/app/reports/<entity>", methods=["POST"])
def get_filtered_report(entity:str):
    validator.validate(entity, str)
    if entity not in data_reposity.keys():
        raise operation_exception("Некорректно указан тип данных! См метод /api/report/entities")
    
    # Получим Dto фильтра
    data = request.get_json()
    convert = convert_factory()
    filterDto = filter()
    convert.deserialize(data, filterDto)
    if len(filterDto.items) == 0:
        raise operation_exception(f"Ошибка при обработке данных! Некорректно передан фильтр.")
    
    # Отфильтруем данные
    source_data = reposity.data[ entity ]
    service = filter_service()
    data = service.filter(source_data, filterDto)
    if len(data) == 0:
        return None

    # Сформируем ответ
    report = factory.create_default()
    if report is None:
        raise operation_exception("Невозможно подобрать корректный отчет согласно параметрам!")

    report.create(data)
    return report.result

"""
Изменить дату блокировки
"""
@app.route("/app/data_block//<data_block>", methods=["POST"])
def set_data_block(data_block: datetime):
    validator.validate(data_block, datetime)
    settings_model.data_block(data_block)
    settings_model.save(data_block, "settings.py")
    return 200
    

"""
Получить дату блокировки
"""
@app.route("/app/data_block", methods=["GET"])
def get_data_block():
    return {"dateblock": settings_model.data_block}
    


if __name__ == '__main__':
    app.add_api('swagger.yaml' )
    app.run(port = 8080)

