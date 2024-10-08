                                                                        
import unittest
from Src.settings_manager import settings_manager

"""
Набор тестов для проверки работы с настройками
"""
class test_settings(unittest.TestCase):
    
    """
    Проверить открытие и загрузку настроек с ошибкой
    """
    def test_settings_manager_open_fail(self):
       # Подготовка
       manager1 = settings_manager()

       # Действие
       manager1.open("../settings1.json")

       # Проверки 
       print(manager1.error_text)
       assert manager1.is_error == True


    """
    Проверить открытие и загрузку настроек
    """
    def test_settings_manager_open(self):
       # Подготовка
       manager1 = settings_manager()

       # Действие
       result = manager1.open("../settings.json")

       # Проверки 
       assert result is True
       assert len(manager1.settings.report_handlers) > 0

    """
    Проверить работу шаблона singletone
    """
    def test_settings_manager_singletone(self):
       # Подготовка
       manager1 = settings_manager()
       result = manager1.open("../settings.json")

       # Действие
       manager2 = settings_manager()

       # Проверки
       assert result == True
       assert manager1 == manager2
       assert manager1.settings.inn == manager2.settings.inn
       assert manager1.settings.organization_name == manager2.settings.organization_name

       

if __name__ == '__main__':
    unittest.main()   

