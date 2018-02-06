from rest_framework import serializers
from .models import Location, Result

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'latitude', 'longitude', 'category')
        view_name = 'location-detail'

class ResultSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    distance = serializers.FloatField()
    category = serializers.CharField(max_length=256)