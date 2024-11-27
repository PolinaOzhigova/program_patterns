from Src.data_reposity import data_reposity
from Src.Core.event_type import event_type
from Src.Logics.observe_service import observe_service

class log_service():
    __reposity: data_reposity = None

    def made_log(self, text_log, log_type):
        observe_service.raise_event(event_type.log_type, None)
    
    