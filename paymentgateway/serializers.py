from rest_framework import serializers
from .models import *

class TransactionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionRequest
        fields = '__all__'


class TransactionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionResponse
        fields = '__all__'

