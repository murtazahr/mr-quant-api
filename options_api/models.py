import quantsbin.derivativepricing as qbdp
from typing import List, Tuple
from .enums import PricingModel
from .utils import date_utils


# Create your models here.
class PricingEngine:
    def __init__(self, model: PricingModel, spot: float, fwd: float,
                 rf_rate: float, volatility: float, yield_div: float, div_list: List[Tuple[str, float]],
                 pricing_date: str = date_utils.current_dt_as_string(date_utils.QUANTSBIN_FORMAT)):
        self.model = model
        self.spot = spot
        self.fwd = fwd
        self.rf_rate = rf_rate
        self.volatility = volatility
        self.yield_div = yield_div
        self.div_list = div_list
        self.pricing_date = pricing_date


class PricingPackage:
    def __init__(self, instruments: List[qbdp.EqOption], pricing_engine: PricingEngine):
        self.instruments = instruments
        self.pricing_engine = pricing_engine
