from django.http import HttpResponseNotAllowed
from functools import wraps
def OnlyGetRequest(func):
    @wraps(func)
    def execute(*args, **kwargs):
        if args[0].method=="GET":
            return func(*args, **kwargs)
        return HttpResponseNotAllowed(["POST"])
    return execute