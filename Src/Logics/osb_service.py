from Src.data_reposity import data_reposity
from Src.Core.validator import validator
from Src.Logics.observe_service import observe_service
from Src.Core.event_type import event_type

class osb_service():
    __reposity: data_reposity = None

    def __init__(self, reposity: data_reposity) -> None:
        super().__init__()
        validator.validate(reposity, data_reposity)
        self.__reposity = reposity

    
    def get_osb_report(self):
        if "osb_key" in data_reposity.keys():
            result = self.__reposity.data[data_reposity.osb_key()]
        else:
            observe_service.raise_event(event_type.OSB, self.__reposity.data[data_reposity.warehouse_transaction_key()])
            result = self.__reposity.data[data_reposity.osb_key()]

        return result