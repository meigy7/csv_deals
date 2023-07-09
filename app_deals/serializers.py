from rest_framework import serializers
from django.db.models import Sum, Count
from django.db.models.functions import Concat
from .models import Deal, File_load, User, Gem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name']

class GemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gem
        fields = ['name']


class File_loadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_load
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    u_name = UserSerializer(many=True, read_only=True)
    gems = serializers.ListField(read_only=True)
    class Meta:
        model = Deal
        fields = ('username', 'u_name', 'gem', 'gems', 'spent_money')











    # u_name = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='name'
    # )
    # username = serializers.SerializerMethodField('get_username_name')
    # gem = serializers.SerializerMethodField('get_gem_name')
    # u_name = serializers.CharField(source='username.name', read_only=True)
    # spent_money2 = serializers.FloatField(read_only=True)