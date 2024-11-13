from enum import Enum
from Src.Core.validator import validator

"""
Event type Enum
"""
class event_type(Enum):
    DELETE_NOMENCLATURE = 1
    CHANGE_NOMENCLATURE = 2
    CHANGE_RANGE = 3
    CHANGE_BLOCK_PERIOD = 4
    FIRST_START = 5