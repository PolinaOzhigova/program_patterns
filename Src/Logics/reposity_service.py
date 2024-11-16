from Src.data_reposity import data_reposity
from Src.Core.validator import validator
from Src.Logics.observe_service import observe_service
from Src.Core.event_type import event_type
import json

class reposity_service():
    __reposity: data_reposity = None

    def __init__(self, reposity: data_reposity) -> None:
        super().__init__()
        validator.validate(reposity, data_reposity)
        self.__reposity = reposity

    def load_data(self):
        with open('data_reposity.json', 'w') as f:
            json.dump(self.__data, f)
        observe_service.raise_event(event_type.FIRST_START, None)
        
    
    def upload_data(self):
        with open('data_reposity.json') as f:
            self.__data = json.load(f)