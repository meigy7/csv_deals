from rest_framework import serializers
from .models import Deal, File_load


class File_loadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File_load
        fields = '__all__'


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ('time_deal', 'username', 'gem', 'quantity', 'spent_money')

    # time_deal = serializers.DateTimeField()
    # username = serializers.CharField(max_length=100)
    # gem = serializers.CharField(max_length=100)
    # quantity = serializers.IntegerField()
    # spent_money = serializers.FloatField()
    
    def create(self, validated_data):
        """
        Create and return a new `Deal` instance, given the validated data.
        """
        return Deal.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Deal` instance, given the validated data.
        """
        instance.time_deal = validated_data.get('time_deal', instance.time_deal)
        instance.username = validated_data.get('username', instance.username)
        instance.gem = validated_data.get('gem', instance.gem)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.spent_money = validated_data.get('spent_money', instance.spent_money)
        instance.save()
        return instance


# class DealSortSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     class Meta:
#         model = Deal
#         fields = ('username', 'spent_money', '')


