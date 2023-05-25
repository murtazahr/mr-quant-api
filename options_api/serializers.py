from rest_framework import serializers
import quantsbin.derivativepricing as qbdp
from .enums import PricingModel


class EqOptionSerializer(serializers.Serializer):
    option_type = serializers.CharField(default='Call')
    expiry_type = serializers.CharField(default='European')
    strike = serializers.FloatField()
    expiry_date = serializers.DateField()
    derivative_type = serializers.CharField(default='Vanilla Option')

    def create(self, validated_data):
        return qbdp.EqOption(**validated_data)


class DivListTupleSerializer(serializers.Serializer):
    element1: serializers.CharField()
    element2: serializers.FloatField()


class PricingEngineSerializer(serializers.Serializer):
    model = serializers.ChoiceField(choices=[(member.value, member.name) for member in PricingModel])
    spot = serializers.FloatField()
    fwd = serializers.FloatField()
    rf_rate = serializers.FloatField()
    volatility = serializers.FloatField()
    yield_div = serializers.FloatField()
    div_list = DivListTupleSerializer(many=True)
    pricing_date = serializers.CharField()


class PricingPackageSerializer(serializers.Serializer):
    instruments = EqOptionSerializer(many=True)
    pricing_engine = PricingEngineSerializer(many=False)
