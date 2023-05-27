from rest_framework import serializers
import quantsbin.derivativepricing as qbdp
from .enums import MarketType


class EqOptionSerializer(serializers.Serializer):
    option_type = serializers.CharField(default='Call')
    expiry_type = serializers.CharField(default='European')
    strike = serializers.FloatField()
    expiry_date = serializers.DateField()
    derivative_type = serializers.CharField(default='Vanilla Option')

    def create(self, validated_data):
        return qbdp.EqOption(**validated_data)


class PricingContextSerializer(serializers.Serializer):
    market_type = serializers.ChoiceField(choices=[(member.value, member.name) for member in MarketType])
    pos_date = serializers.CharField()


class PricingPackageSerializer(serializers.Serializer):
    instruments = EqOptionSerializer(many=True)
    pricing_context = PricingContextSerializer(many=False)
