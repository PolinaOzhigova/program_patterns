from Src.Core.validator import validator
from Src.Models.warehouse_transactions import warehouse_transaction
from Src.data_reposity import data_reposity
from Src.Core.event_type import event_type
from Src.Core.abstract_observe import absrtact_observe


class observe_osb(absrtact_observe):
    """Наблюдатель"""
    def handle_event(self, type: event_type, params ):
        super().handle_event(type, params)       

        if type == event_type.OSB:
            dates = {}
            result = []

            for transaction in params:
                validator.validate(transaction, warehouse_transaction)
                warehouse1 = transaction.warehouse
                if warehouse1.address in dates.keys():
                    result.append([dates.get(warehouse1.address), None, warehouse1, transaction])
                    dates.update(warehouse1.address, transaction.period)
                else:
                    dates.update(warehouse1.address, transaction.period)
            for res in result:
                for keys in dates:
                    if keys == res[2]:
                        res[1] = dates.get(warehouse1.address)

            self.reposity.data[data_reposity.osb_key()] = result
            return result