from django.http import HttpResponseNotAllowed
from functools import wraps
from doctor.models import DoctorModel
def OnlyAuthenticatedDoctor(func):
    @wraps(func)
    def execute(request,*args, **kwargs):
        try:
            doctroObject=DoctorModel.objects.get(pk=request.session["doctor_id"])
            return func(request,*args, **kwargs)
        except DoctorModel.DoesNotExist:
            return HttpResponseNotAllowed(["POST"])
    return execute