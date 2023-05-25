from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers import PricingPackageSerializer


class PricingApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PricingPackageSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
