from rest_framework import serializers
from .models import patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = patient
        fields = '__all__'  # or list specific fields: ['id', 'name', ...]
