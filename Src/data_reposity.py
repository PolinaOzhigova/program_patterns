from Src.Core.abstract_logic import abstract_logic
from datetime import datetime
from Src.Logics.observe_service import observe_service
from Src.Core.event_type import event_type
import json
from Src.settings_manager import settings_manager

"""
Репозиторий данных
"""
class data_reposity(abstract_logic):
    __data = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(data_reposity, cls).__new__(cls)
        return cls.instance 

    """
    Набор данных
    """
    @property
    def data(self) :
        return self.__data

    """
    Ключ для хранения групп номенклатуры
    """
    @staticmethod
    def group_key() -> str:
        return "group_model"
    
    """
    Ключ для хранения номенклатуры
    """
    @staticmethod
    def nomenclature_key() -> str:
        return "nomenclature_model"
    
    """
    Ключ для хранения единиц измерения
    """
    @staticmethod
    def range_key() -> str:
        return "range_model"
    
    """
    Ключ для хранения рецептов
    """
    @staticmethod
    def receipt_key() -> str:
        return "receipt_model"
    
    
    """
    Ключ для хранения складов
    """
    @staticmethod
    def warehouse_key() -> str:
        return "warehouse"
    
    """
    Ключ для хранения транзакций складов
    """
    @staticmethod
    def warehouse_transaction_key() -> str:
        return "warehouse_transaction"
    
    """
    Ключ для хранения расчета процессов
    """
    @staticmethod
    def turnover_process_key():
        return "turnover_process"
    
    """
    Получить список всех ключей
    Источник: https://github.com/Alyona1619
    """
    @staticmethod
    def keys() -> list:
        result = []
        methods = [method for method in dir(data_reposity) if
                    callable(getattr(data_reposity, method)) and method.endswith('_key')]
        for method in methods:
            key = getattr(data_reposity, method)()
            result.append(key)

        return result
    
    """
    Перегрузка абстрактного метода
    """
    def set_exception(self, ex: Exception):
        self._inner_set_exception(ex)    

    """Наблюдатель"""
    def handle_event(self, type: event_type, params ):
        super().handle_event(type, params)       

        if type == event_type.FIRST_START:
            manager = settings_manager()
            manager.start = False
            self.save(self.__file_name)

    def upload_data(self):
        with open('data_reposity.json', 'w') as f:
            json.dump(self.__data, f)
        self.handle_event(event_type.FIRST_START, None)
    
    def load_data(self):
        with open('data_reposity.json') as f:
            self.__data = json.load(f)
        self.handle_event(event_type.FIRST_START, None)