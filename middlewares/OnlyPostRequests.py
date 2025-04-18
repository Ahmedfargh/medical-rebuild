from django.http import HttpResponseNotAllowed
from functools import wraps
def OnlyPostRequest(func):
    @wraps(func)
    def execute(*args, **kwargs):
        if args[0].method=="POST":
            return func(*args, **kwargs)
        return HttpResponseNotAllowed(["POST"])
    return execute