#!/usr/bin/python

from scipy.stats import norm
from scipy.optimize import brentq
import numpy as np


def BlackOverK(moneyness, stdDev, callOrPut):
    d1 = np.log(moneyness) / stdDev + stdDev / 2.0
    d2 = d1 - stdDev
    return callOrPut * (moneyness*norm.cdf(callOrPut*d1)-norm.cdf(callOrPut*d2))

def Black(strike, forward, sigma, T, callOrPut):
    return strike * BlackOverK(forward/strike,sigma*np.sqrt(T),callOrPut)

def BlackImpliedVol(price, strike, forward, T, callOrPut):
    def objective(sigma):
        return Black(strike, forward, sigma, T, callOrPut) - price
    return brentq(objective,0.01, 1.00, xtol=1.0e-8)

def BachelierRaw(moneyness, stdDev, callOrPut):
    h = callOrPut * moneyness / stdDev
    return stdDev * (h*norm.cdf(h) + norm.pdf(h))

def Bachelier(strike, forward, sigma, T, callOrPut):
    return BachelierRaw(forward-strike,sigma*np.sqrt(T),callOrPut)

def BachelierImpliedVol(price, strike, forward, T, callOrPut):
    def objective(sigma):
        return Bachelier(strike, forward, sigma, T, callOrPut) - price
    return brentq(objective,0.01*forward, 1.00*forward, xtol=1.0e-8)

