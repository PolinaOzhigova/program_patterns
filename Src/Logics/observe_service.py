from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type

class observe_service():
    observers = []

    @staticmethod
    def append(service: abstract_logic):

        if service is None:
            return

        if not isinstance(service, abstract_logic):
            return

        items =  list(map( lambda x: type(x).__name__,  observe_service.observers))
        found =    type( service ).__name__ in items 
        if not found: 
            observe_service.observers.append( service )

    @staticmethod
    def raise_event( type: event_type, params ):
        for observer in observe_service.observers:
            if observer is not None:
                observer.handle_event( type, params )   
        return True
    
