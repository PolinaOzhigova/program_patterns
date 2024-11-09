from Src.data_reposity import data_reposity
from Src.Core.validator import validator
from Src.Models.nomenclature import nomenclature_model
from Src.Logics.filter_prototype import filter_prototype
from Src.Core.condition_type import condition_type
from Src.Logics.observe_service import observe_service
from Src.Core.event_type import event_type

class nomenclature_service():
    __reposity: data_reposity = None
    __nomenclature_key: str = None

    def __init__(self, reposity: data_reposity) -> None:
        super().__init__()
        validator.validate(reposity, data_reposity)
        self.__reposity = reposity
    
    def put(self, item_nomenclature):
        self.__reposity.data[data_reposity.nomenclature_key()].append(item_nomenclature)
        return

    def get(self, id_nomenclature):
        all_data = self.__reposity.data[data_reposity.nomenclature_key()]
        prototype = filter_prototype(all_data)
        result = prototype.create("unique_code", condition_type.EQUALS, id_nomenclature)
        return result[0]
    
    def update(self, item_nomenclature):
        old_nomenclature = self.get(item_nomenclature.unique_code)
        for attr, value in vars(item_nomenclature).items():
            setattr(old_nomenclature, attr, value)
        observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, item_nomenclature)
        return

    def delete(self, id_nomenclature):
        item = self.get(id_nomenclature.unique_code)
        observe_service.raise_event(event_type.DELETE_NOMENCLATURE, item)