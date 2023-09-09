from rest_framework import serializers
from .models import *

class AutoTimeStampModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutoTimeStampModel
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = "__all__"
