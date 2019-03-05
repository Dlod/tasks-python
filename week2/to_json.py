# coding: utf-8

import json
from functools import wraps

def to_json(fun):
    @wraps(fun)
    def decorator(*args, **kwargs):
        return json.dumps(fun(*args, **kwargs))
    return decorator

@to_json
def get_data():
  return {"data": 42}
  
  
get_data()  # вернёт '{"data": 42}'

