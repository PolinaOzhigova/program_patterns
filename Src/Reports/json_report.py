from Src.Core.convert_factory import convert_factory
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import operation_exception, validator
import json


"""
Простой отчет для формирования данных в формате Json
"""
class json_report(abstract_report):

    def __init__(self) -> None:
       super().__init__()

 
    """
    Сформировать отчет.
    """
    def create(self, data: list):
        validator.validate(data, list)
        if len(data) == 0:
            raise operation_exception("Набор данных пуст!")
        
        factory = convert_factory()
        items = factory.serialize(data)

        if factory.is_error:
            raise operation_exception(factory.error_text)
        
        self.result = json.dumps(items, ensure_ascii=False, indent=4)


