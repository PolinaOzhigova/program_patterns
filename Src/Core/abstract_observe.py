from abc import ABC, abstractmethod

class absrtact_observe(ABC):
    
    @abstractmethod
    def handle_event(_type, params):
        pass
