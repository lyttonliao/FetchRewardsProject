from rest_framework import serializers

from core.models import Payer


class PayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payer
        fields = ('id', 'company',)