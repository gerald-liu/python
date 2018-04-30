# FINA 3203 – Derivative Securities, Spring 2018, HKUST
# Assignment 6 (calculations)
# Author: Gerald Liu

import math
from scipy.stats import norm


def d1(s, k, r, sigma, tau):
    if sigma == 0 or tau == 0: return None
    return (math.log(s/k)+(r+0.5*sigma**2)*tau)/(sigma*math.sqrt(tau))

def d2(s, k, r, sigma, tau):
    if sigma == 0 or tau == 0: return None
    return d1(s, k, r, sigma, tau)-sigma*math.sqrt(tau)

def bsm(callFlag, s, k, r, sigma, tau): # callFlag = 1 means call option
    if sigma == 0 or tau == 0: return s
    if callFlag:
        return s*norm.cdf(d1(s, k, r, sigma, tau))-k*math.exp(-r*tau)*norm.cdf(d2(s, k, r, sigma, tau))
    else:
        return k*math.exp(-r*tau)*norm.cdf(-d2(s, k, r, sigma, tau))-s*norm.cdf(-d1(s, k, r, sigma, tau))

def edf(v, f, r, sigma, t):
    if sigma == 0 or t == 0: return 0
    return norm.cdf(-d2(v, f, r, sigma, t))
    
def equityMerton(v, f, r, sigma, t): return bsm(1, v, f, r, sigma, t)
    
def debtMerton(v, f, r, sigma, t):
    if sigma == 0 or t == 0: return v
    return f*math.exp(-r*t)-bsm(0, v, f, r, sigma, t)

def creditSpread(v, f, r, sigma, t):
    return -(math.log(debtMerton(v/f, 1, r, sigma, t)))/t-r

def expectedLoss(v, f, mu, sigma, t):
    return bsm(0, v, f, mu, sigma, t) * math.exp(mu*t) / edf(v, f, mu, sigma, t)

def approxCreditSpread(v, f, r, mu, sigma, t):
    return expectedLoss(v, f, mu, sigma, t)/f * edf(v, f, r, sigma, t) / t


v = 100
sigma = 0.4
mu = 0.15
r = 0.08


# Question 1

f_0 = 0.5 * 120
t = 5
edf_0 = edf(v, f_0, r, sigma, t)
cs_0 = creditSpread(v, f_0, r, sigma, t)
print ("Question 1\nThe probability of default EDF = {:.2%}\nThe credit spread = {:.2%}".format(edf_0, cs_0))


# Question 2

print ("\n\nQuestion 2")
f_1 = 100

for t in [1, 3, 10]:
    if t <= 1:
        f = f_0 + f_1
    else:
        f = f_0 + 0.5*f_1
    edf_1 = edf(v, f, r, sigma, t)
    cs_1 = creditSpread(v, f, r, sigma, t)
    el_1 = expectedLoss(v, f, mu, sigma, t)
    acs_1 = approxCreditSpread(v, f, r, mu, sigma, t)
    print("For T = {}:".format(t))
    print("The credit spread is {:.2%}, the probability of default is {:.2%}.".format(cs_1, edf_1))
    print("The expected loss given default is ${:.2f}.".format(el_1))
    print("The approximated credit spread given default is {:.2%}, the absolute and relative errors are {:.2%}, {:.2%} respectively.\n".format(acs_1, acs_1-cs_1, (acs_1-cs_1)/cs_1))


# Question 3

f_2 = 110
t = 3
f = f_0 + 0.5*f_2
cs_2 = creditSpread(v, f, r, sigma, t)
y = r + cs_2
b = math.exp(-y*t)*f_2
edf_2 = edf(v, f, r, sigma, t)
delta = f - bsm(0, v, f, mu, sigma, t) * math.exp(mu*t) / edf(v, f, mu, sigma, t)
print("\n\nQuestion 3\nThe bond price is ${:.2f}, YTM is {:.2%}, default probability is {:.2%}, expected recovery is ${:.2f}.".format(b, y, edf_2, delta))
