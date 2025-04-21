from django.core.cache import cache
from functools import wraps

def freshCache(func):
    @wraps(func)
    def execute(request,*args, **kwargs):
        cache.set("doctor_"+str(request.session["doctor_id"])+"_is_loged",True,5)
        return func(request,*args, **kwargs)
    return execute