from rest_framework import serializers
from .models import Deal, File_load, User, Gem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']

class GemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gem
        fields = '__all__'

class File_loadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_load
        fields = '__all__'

class DealSerializer(serializers.ModelSerializer):
    gems = serializers.ListField(child=serializers.CharField())
    class Meta:
        model = Deal
        fields = ('username', 'spent_money', 'gems')

class DealSerializer_top(serializers.Serializer):
    username = serializers.CharField()
    spent_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    gems = serializers.ListField(child=serializers.CharField())
    class Meta:
        fields = ('username', 'spent_money', 'gems')
