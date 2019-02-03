#%%
from scipy.stats import norm

#%%
print('{:.4f}'.format(1-norm.cdf(1.5)))

#%%
print('{:.4f}'.format((2*norm.ppf(0.9))+12))