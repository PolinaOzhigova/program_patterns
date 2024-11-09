from Src.Core.abstract_observe import absrtact_observe
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity

class observe(absrtact_observe) :
    __events = {}
    __reposity: data_reposity = None

    def __init__(self) -> None:
        super().__init__()
        self.__events[event_type.CHANGE_NOMENCLATURE] = self.change_event
        self.__events[event_type.DELETE_NOMENCLATURE] = self.delete_event

    def handle_event(self, _type, params):
        self.__events[_type](params)

    def change_event(self, params):
        all_data = self.__reposity.data[data_reposity.receipt_key]
        for receipt in all_data:
            for ing in receipt.ingridients:
                for nomenc in ing.nomeclature:
                    for attr, value in vars(params).items():
                        setattr(nomenc, attr, value)

    def delete_event(self, params):
        all_data = self.__reposity.data[data_reposity.receipt_key]
        for receipt in all_data:
            for ing in receipt.ingridients:
                for nomenc in ing.nomeclature:
                    pass
