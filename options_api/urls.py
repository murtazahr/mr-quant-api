from django.urls import path, include
from .controllers.pricing_controller import PricingApiView

urlpatterns = [
    path('pricing', PricingApiView.as_view())
]
