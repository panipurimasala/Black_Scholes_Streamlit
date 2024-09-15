import math
from scipy.stats import norm
class Bschole_calc(object):
    #initializes the strike object
    def __init__(self, strike_price,current_price, ttm, vol, risk_free_rate, type_of_security):
        self.strike = strike_price
        self.curr = current_price
        self.ttm = ttm
        self.vol = vol
        self.rfr = risk_free_rate
        self.type = type_of_security
    #calculation of the black scholes using the prices above
    def __calc__(self):
        d1 = (math.log(self.curr/self.strike) + (self.rfr+((self.vol)**2)/2)*self.ttm)/(self.vol*((self.ttm)**0.5))
        d2 = d1 - self.vol * math.sqrt(self.ttm)

        if self.type == "Call":
            return float(self.curr*(norm.cdf(d1)) - self.strike*math.exp(-1*self.rfr*self.ttm) * (norm.cdf(d2)))
        elif self.type=='Put':
            return float(self.strike*math.exp(-1*self.rfr*self.ttm) * (norm.cdf(-d2)) - self.curr*(norm.cdf(-d1)))
        else:
            raise ValueError("Invalid option type. Use 'Call' or 'Put'.")