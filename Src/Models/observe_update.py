from Src.Core.abstract_observe import absrtact_observe
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity

class observe_update(absrtact_observe) :
    reposity: data_reposity = None
    _type :event_type = None

    def handle_event(self, _type, params):
        if self._type != event_type.CHANGE_NOMENCLATURE:
            return
        all_data = self.reposity.data[data_reposity.receipt_key]
        for receipt in all_data:
            for ing in receipt.ingridients:
                for nomenc in ing.nomeclature:
                    for attr, value in vars(params).items():
                        setattr(nomenc, attr, value)
        
