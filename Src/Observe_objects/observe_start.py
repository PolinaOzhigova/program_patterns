from Src.Core.event_type import event_type
from Src.Core.abstract_observe import absrtact_observe
from Src.settings_manager import settings_manager

class observe_start(absrtact_observe):
    """Наблюдатель"""
    def handle_event(self, type: event_type, params ):
        super().handle_event(type, params)       

        if type == event_type.FIRST_START:
            manager = settings_manager()
            manager.start = False
            self.save(self.__file_name)