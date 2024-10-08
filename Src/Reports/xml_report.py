from Src.Core.convert_factory import convert_factory
from Src.Core.abstract_report import abstract_report
from Src.Core.validator import operation_exception, validator
from dict2xml import dict2xml
# https://www.geeksforgeeks.org/serialize-python-dictionary-to-xml/

"""
Простой отчет для формирования данных в формате Json
"""
class xml_report(abstract_report):

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
        result = dict2xml(items, wrap = data[0].__class__.__name__, indent ="   ")
        self.result = f'<?xml version="1.0"?>\n<root>\n{result}\n</root>'