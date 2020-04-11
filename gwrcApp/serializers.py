from rest_framework import serializers
from .models import Alarm


class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = ['alarm_id', 'created_date', 'type', 'message']
