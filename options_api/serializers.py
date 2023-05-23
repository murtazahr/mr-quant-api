from rest_framework import serializers
import quantsbin.derivativepricing as qbdp


class EqOptionSerializer(serializers.Serializer):
    option_type = serializers.CharField(default='Call')
    expiry_type = serializers.CharField(default='European')
    strike = serializers.FloatField()
    expiry_date = serializers.DateField()
    derivative_type = serializers.CharField(default='Vanilla Option')

    def create(self, validated_data):
        return qbdp.EqOption(**validated_data)