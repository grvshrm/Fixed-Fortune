import numpy as np
import scipy.optimize as optimize
import pandas as pd

class RiskCalculator:
    def __init__(self, bond_data):
        self.bond_data = bond_data

    def bond_ytm(self, price, coup, par, T, freq = 2, guess = 0.05):
        freq = float(freq)
        periods = T * 2
        coupon = coup/100. * par
        dt = [(i + 1)/freq for i in range(int(periods))]
        ytm_func = lambda y: sum([coupon/freq/(1+y/freq)**(freq*t) for t in dt]) + par/(1+y/freq)**(freq*T) - price
        return optimize.newton(ytm_func, guess)
    
    def bond_price(self, par, T, ytm, coup, freq = 2):
        freq = float(freq)
        periods = T * 2
        coupon = coup/100.*par
        dt = [(i+1)/freq for i in range(int(periods))]
        price = sum([coupon/freq/(1+ytm/freq)**(freq*t) for t in dt]) + par/(1+ytm/freq)**(freq*T)
        return price
    
    def bond_mod_duration(self, price, coup, par, T, ytm, freq = 2, dy = 0.01):
        ytm_minus = ytm - dy
        price_minus = self.bond_price(par, T, ytm_minus, coup, freq)
        
        ytm_plus = ytm + dy
        price_plus = self.bond_price(par, T, ytm_plus, coup, freq)
        
        mduration = (price_minus - price_plus)/(2 * price * dy)
        return mduration
    
    def bond_convexity(self, price, coup, par, T, ytm, freq = 2, dy = 0.01):
        ytm_minus = ytm - dy
        price_minus = self.bond_price(par, T, ytm_minus, coup, freq)
        
        ytm_plus = ytm + dy
        price_plus = self.bond_price(par, T, ytm_plus, coup, freq)
        
        convexity = (price_minus + price_plus - 2 * price)/(price*dy**2)
        return convexity
    
    def calculate_risk(self):
        self.bond_data["ytm"] = self.bond_data.apply(lambda row: self.bond_ytm(row['bond_price'], row['coupon_rate'], row['face_value'], row['time_period']), axis = 1)
        self.bond_data["mdur"] = self.bond_data.apply(lambda row: self.bond_mod_duration(row['bond_price'], row['coupon_rate'], row['face_value'], row['time_period'], row['ytm']), axis = 1)
        self.bond_data["conv"] = self.bond_data.apply(lambda row: self.bond_convexity(row['bond_price'], row['coupon_rate'], row['face_value'], row['time_period'], row['ytm']), axis = 1)
        return self.bond_data