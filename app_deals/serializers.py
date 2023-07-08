from rest_framework import serializers
from .models import Deal, File_load


class File_loadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_load
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'


# class DealSortSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     class Meta:
#         model = Deal
#         fields = ('username', 'spent_money', 'gem')