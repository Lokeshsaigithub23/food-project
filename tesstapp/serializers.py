from rest_framework import serializers
from .models import restaurant,fooditem
class fooditemSerializer(serializers.ModelSerializer):
    class Meta:
        model=fooditem
        fields='__all__'

class restaurantSerializer(serializers.ModelSerializer):
    menu=fooditemSerializer(many=True,read_only=True)
    class Meta:
        model=restaurant
        fields='__all__'
