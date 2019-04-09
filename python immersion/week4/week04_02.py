class Value:
    def __init__(self):
        self.value = None
    @staticmethod
    def _prepare_value(value, commission):
        return value - commission * value

    def __get__(self, obj, obj_type):
        return self.value
 
    def __set__(self, obj, value):
        self.value = int(self._prepare_value(value, obj.commission)) if str(self._prepare_value(value, obj.commission)).split(".")[1] == '0' else self._prepare_value(value, obj.commission)

class Account:
    amount = Value()
    
    def __init__(self, commission):
        self.commission = commission


