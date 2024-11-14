from Src.Core.abstract_observe import absrtact_observe
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity

class observe_delete(absrtact_observe) :
    reposity: data_reposity = None

    def handle_event(self, _type, params):
        if _type != event_type.DELETE_NOMENCLATURE:
            return

        all_data = self.reposity.data[data_reposity.receipt_key]

        stop_word = False
        for receipt in all_data:
            if stop_word:
                break
            for ing in receipt.ingridients:
                if stop_word:
                    break
                for nomenc in ing.nomeclature:
                    if(nomenc == params):
                        stop_word = True
        else:
            all_data.remove(params)
