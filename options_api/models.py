import quantsbin.derivativepricing as qbdp
from typing import List
from .enums import MarketType


# Create your models here.
class PricingContext:
    def __init__(self, market_type: MarketType, pos_date: str):
        self.market_type = market_type
        self.pos_date = pos_date


class PricingPackage:
    def __init__(self, instruments: List[qbdp.EqOption], pricing_context: PricingContext):
        self.instruments = instruments
        self.pricing_context = pricing_context
