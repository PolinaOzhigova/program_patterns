from Src.Core.abstract_observe import absrtact_observe
from Src.Core.event_type import event_type
from Src.data_reposity import data_reposity

class observe_log(absrtact_observe) :
    reposity: data_reposity = None

    def handle_event(self, _type, params):
        if _type != event_type.INFO or _type != event_type.DEBUG or _type != event_type.ERROR:
            return


