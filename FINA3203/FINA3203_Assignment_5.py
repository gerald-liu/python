# FINA 3203 – Derivative Securities, Spring 2018, HKUST
# Assignment 5 (calculations)
# Author: Gerald Liu

import math
from scipy.stats import norm
from scipy.special import binom
from scipy.optimize import brentq


def optPayoff(callFlag, s, k):
    return max(s-k, 0) if callFlag else max(k-s, 0)

def putCallParity(callFlag, priceGiven, s, k, r, t): # callFlag = 1 means get call from put
    if callFlag:
        return priceGiven - (k*math.exp(-r*t) - s)
    else:
        return priceGiven + (k*math.exp(-r*t) - s)

def d1(s, k, r, sigma, tau):
    if sigma == 0 or tau == 0: return None
    return (math.log(s/k)+(r+0.5*sigma**2)*tau)/(sigma*math.sqrt(tau))

def d2(s, k, r, sigma, tau):
    if sigma == 0 or tau == 0: return None
    return d1(s, k, r, sigma, tau)-sigma*math.sqrt(tau)

def bsm(callFlag, s, k, r, sigma, tau): # callFlag = 1 means call option
    if sigma == 0 or tau == 0: return 0
    if callFlag:
        return s*norm.cdf(d1(s, k, r, sigma, tau))-k*math.exp(-r*tau)*norm.cdf(d2(s, k, r, sigma, tau))
    else:
        return k*math.exp(-r*tau)*norm.cdf(-d2(s, k, r, sigma, tau))-s*norm.cdf(-d1(s, k, r, sigma, tau))

def stockChange(upNum, downNum, sigma, t):
    return math.exp(sigma*math.sqrt(t/(upNum+downNum)))**(upNum-downNum)

def riskNeutralProb(callFlag, r, sigma, t, n):
    up = math.exp(sigma*math.sqrt(t/n)) # 1+u
    if callFlag:
        return (math.exp(r*t/n)-1/up)/(up-1/up)
    else:
        return (math.exp(r*t/n)-up)/(1/up-up)
    
def riskNeutralPrice(callFlag, h, q, up, down):
    if callFlag:
        return math.exp(-r*h)*(q*up + (1-q)*down)
    else:
        return math.exp(-r*h)*(q*down + (1-q)*up)


class OptNode:
    def __init__(self, stock, option, up, down):
        self.stock = stock
        self.option = option
        self.up = up          # left node
        self.down = down      # right node
    
    def copy(self, another):
        self.stock = another.stock
        self.option = another.option
        self.up = another.up
        self.down = another.down

class OptTree:
    def __init__(self, EuFlag, callFlag, s, k, r, sigma, t, n):
        self.EuFlag = EuFlag
        self.callFlag = callFlag
        self.s = s
        self.k = k
        self.r = r
        self.sigma = sigma
        self.t = t
        self.n = n
        self.q = riskNeutralProb(callFlag, r, sigma, t, n)
        self.upPct = math.exp(sigma*math.sqrt(t/n)) # 1+u
        self.root = OptNode(0, 0, None, None)
    
    def build(self):
        h = t / n
        nodes = []
        for i in range(self.n, -1, -1):
            level = []
            if i == self.n:
                for j in range(0, i + 1):
                    stock = self.s * self.upPct**(2*j-self.n)
                    level.append(OptNode(stock, optPayoff(self.callFlag, stock, self.k), None, None))
            else:
                for j in range(0, i + 1):
                    upNode = nodes[-1][j + 1]
                    downNode = nodes[-1][j]
                    stock = downNode.stock * self.upPct
                    if EuFlag:
                        level.append(OptNode(stock, riskNeutralPrice(self.callFlag, h, self.q, upNode.option, downNode.option), upNode, downNode))
                    else:
                        level.append(OptNode(stock, max(riskNeutralPrice(self.callFlag, h, self.q, upNode.option, downNode.option), optPayoff(self.callFlag, stock, self.k)), upNode, downNode))
                    
            nodes.append(level)
        
        self.root.copy(nodes[-1][-1])
        return self.root.option
            
def binomTree(EuFlag, callFlag, s, k, r, sigma, t, n):
    bt = OptTree(EuFlag, callFlag, s, k, r, sigma, t, n)
    return bt.build()


class BSM:
    def __init__(self, callFlag, s, k, r, sigma, tau, mkt):
        self.callFlag = callFlag
        self.s = s
        self.k = k
        self.r = r
        self.sigma = sigma
        self.tau = tau
        self.mkt = mkt
        
    def bsmVol(self, vol):
        return bsm(self.callFlag, self.s, self.k, self.r, vol, self.tau) - self.mkt
    
def impliedVol(callFlag, s, k, r, tau, mkt):
    model = BSM(callFlag, s, k, r, 0, tau, mkt)
    if callFlag:
        ub = model.s
        lb = max(0, ub - model.k*math.exp(-model.r*model.tau))
    else:
        ub = model.k*math.exp(-model.r*model.tau)
        lb = max(0, ub - model.s)
    if ub * lb > 0:
        if abs(lb) > abs(ub):
            lb = 0
        else:
            ub = 0
    return brentq(model.bsmVol, lb, ub)


# Question 1
EuFlag = 1
callFlag = 0
s = 100
k = 100
sigma = 0.25
r = 0.05
t = 0.75

# 1.1
tau = t - 0
p_bsm = bsm(callFlag, s, k, r, sigma, tau)
print ("Question 1.1\nBy Black-Scholes-Merton model, P = ${:.2f}".format(p_bsm))

# 1.2
n = 3
p_ebt = binomTree(EuFlag, callFlag, s, k, r, sigma, t, n)
print("\nQuestion 1.2\nBy binomial pricing, the European option price is P = ${:.2f}".format(p_ebt))

# 1.3
print("\nQuestion 1.3\nArbitrage profit = ${:.2f}".format(p_ebt - 6))

# 1.4
EuFlag = 0
p_abt = binomTree(EuFlag, callFlag, s, k, r, sigma, t, n)
print("\nQuestion 1.4\nBy binomial pricing, the American option price P = ${:.2f}".format(p_abt))


# Question 2
EuFlag = 1
callFlag = 1
s = 80
k = 80
sigma = 0.25
r = 0.03
t = 1

# 2.1
print("\n\nQuestion 2.1\nBy binomial pricing, the European call price is as follows.")
print("The corresponding put price is given by put-call parity.")
for n in [5, 10, 50, 100]:
    c_ebt = binomTree(EuFlag, callFlag, s, k, r, sigma, t, n)
    print("For N = {}, C = ${:.3f}, P = ${:.3f}".format(n, c_ebt, putCallParity(1-callFlag, c_ebt, s, k, r, t)))

c_bsm = bsm(callFlag, s, k, r, sigma, t)
p_bsm = putCallParity(1-callFlag, c_bsm, s, k, r, t)
n = 190
while True:
    c_ebt = binomTree(EuFlag, callFlag, s, k, r, sigma, t, n)
    if abs(c_ebt - c_bsm) < 0.01:
        p_ebt = putCallParity(1-callFlag, c_ebt, s, k, r, t)
        if abs(p_ebt - p_bsm) < 0.01: break
    n = n + 1

print("\nN = {} is needed for penny accuracy.".format(n))
print("For N = {}, C = ${:.4f}, P = ${:.4f}".format(n, c_ebt, p_ebt))
print("The prices calculated using the BSM model are C = ${:.4f}, P = ${:.4f}".format(c_bsm, p_bsm))

# 2.2
EuFlag = 0
callFlag = 0
n = 100
print("\nQuestion 2.2\nBy binomial pricing, the American put price is as follows.")
print("For N = {}, P = ${:.3f}".format(n, binomTree(EuFlag, callFlag, s, k, r, sigma, t, n)))


# Question 3
callFlag = 1
s = 100
k = 100
r = 0.05
t = 0.75
mkt = 14.087

# 3.1
print("\n\nQuestion 3.1\nThe Black-Scholes implied volatility of the call is {:.0%}.".format(impliedVol(callFlag, s, k, r, t, mkt)))

# 3.2
callFlag = 0
impliedVol = 0.3685

p_implied = bsm(callFlag, s, k, r, impliedVol, t)
p_fair = putCallParity(0, mkt, s, k, r, t)
print("\nQuestion 3.2\nFor the put, traded price = ${0:.3f},".format(p_implied), "fair price = ${0:.3f}.".format(p_fair))
if p_implied > p_fair:
    print("Short 1 put, long 1 call, short 1 underlying stock forward.")
    print("The arbitrage profit is ${0:.3f}.".format(p_implied - p_fair))
elif p_implied < p_fair:
    print("Long 1 put, short 1 call, long 1 underlying stock forward.")
    print("The arbitrage profit is ${0:.3f}.".format(p_fair - p_implied))
else:
    print("No arbitrage.")