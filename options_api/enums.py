from enum import Enum


class PricingModel(Enum):
    BSM = 'BSM'
    MC_GBM = 'MC_GBM'
    BINOMIAL = 'BINOMIAL'
