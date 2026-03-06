from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import contactModel

class contactSerializer(serializers.ModelSerializer):
    class Meta:
        model =contactModel
        fields ='__all__'