
# coding: utf-8

# # FINA 3203 Assignment 6
# FINA 3203 &ndash; Derivative Securities, Spring 2018, HKUST  
# LIU Weiyang, 20413306  
# [wliuax@connect.ust.hk](mailto:wliuax@connect.ust.hk)

# **Table of Contents**
# - [Question 1: Credit Spread](#Q1)
# - [Question 2: Expected Loss Given Default](#Q2)
# - [Question 3: Expected Recovery](#Q3)

# In[1]:


import math
import pandas as pd
from scipy.stats import norm


# In[2]:


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

def edf(v, f, mu, sigma, t):
    if sigma == 0 or t == 0: return 0
    return norm.cdf(-d2(v, f, mu, sigma, t))
    
def equityMerton(v, f, r, sigma, t): return bsm(1, v, f, r, sigma, t)
    
def debtMerton(v, f, r, sigma, t):
    if sigma == 0 or t == 0: return v
    return f*math.exp(-r*t)-bsm(0, v, f, r, sigma, t)

def creditSpread(v, f, r, sigma, t):
    return -(math.log(debtMerton(v/f, 1, r, sigma, t)))/t-r

def expectedLoss(v, f, mu, sigma, t):
    return bsm(0, v, f, mu, sigma, t) * math.exp(mu*t) / edf(v, f, mu, sigma, t)

def approxCreditSpread(v, f, mu, sigma, t):
    return expectedLoss(v, f, mu, sigma, t)/f * edf(v, f, mu, sigma, t) / t


# **Firm Information**  
# v = \$100, &sigma; = 40%, &mu; = 15%, q = 0, r = 8%

# <a id='Q1'></a>
# ## Question 1: Credit Spread

# In[3]:


v = 100
sigma = 0.4
mu = 0.15
r = 0.08

# Question 1

f = 120
t = 5
edf_0 = edf(v, f, mu, sigma, t)
cs_0 = creditSpread(v, f, r, sigma, t)
print ("Question 1\nThe probability of default EDF = {:.2%}\nThe credit spread = {:.2%}".format(edf_0, cs_0))


# In[4]:


print(d1(v, f, mu, sigma, t))
print(d2(v, f, mu, sigma, t))
print(norm.cdf(-d1(v, f, mu, sigma, t)))
print(debtMerton(v, f, mu, sigma, t))


# <a id='Q2'></a>
# ## Question 2: Expected Loss Given Default

# In[5]:


# Question 2

print ("\n\nQuestion 2")
f = 100

df = pd.DataFrame(columns=['Probability of Default', 'Expected Loss Given Default', 'Credit Spread',
                           'Approximated Credit Spread', 'Absolute Error', 'Relative Error'])
for t in [1, 3, 10]:
    edf_1 = edf(v, f, mu, sigma, t)
    cs_1 = creditSpread(v, f, r, sigma, t)
    el_1 = expectedLoss(v, f, mu, sigma, t)
    acs_1 = approxCreditSpread(v, f, mu, sigma, t)
    df.loc[t,:] = ([edf_1, el_1, cs_1, acs_1, acs_1-cs_1, (acs_1-cs_1)/cs_1])

display(df)


# <a id='Q3'></a>
# ## Question 3: Expected Recovery

# In[6]:


# Question 3

f = 110
t = 3
cs_2 = creditSpread(v, f, r, sigma, t)
y = r + cs_2
b = math.exp(-y*t)*f
edf_2 = edf(v, f, mu, sigma, t)
delta = f - bsm(0, v, f, mu, sigma, t) * math.exp(mu*t) / edf(v, f, mu, sigma, t)
print("\n\nQuestion 3\nThe bond price is ${:.2f}, YTM is {:.2%}, default probability is {:.2%}, expected recovery is ${:.2f}.".format(b, y, edf_2, delta))


# In[7]:


print(debtMerton(v, f, mu, sigma, t))

