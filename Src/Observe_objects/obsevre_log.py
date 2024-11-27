from Src.Core.abstract_observe import absrtact_observe
from Src.Core.event_type import event_type
from Src.Core.log_type import log_type
from Src.data_reposity import data_reposity
from Src.settings_manager import settings_manager

class observe_log(absrtact_observe) :
    reposity: data_reposity = None
    
    def handle_event(self, _type, params):
        if _type not in log_type:
            return 
        
        
        


