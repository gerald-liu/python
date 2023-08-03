
import numpy as np
import pandas as pd
import sys

if len(sys.argv) == 1:
    n_pulled = 0
else:
    n_pulled = int(sys.argv[1])

print(f'Pulled: {n_pulled}')

n_pity = 50
p_1 = 0.02
p_inc = 0.02

df = pd.DataFrame(
    {
        'p_1': np.concatenate((np.repeat(p_1, n_pity-n_pulled-1),
                               np.arange(p_1, 1+p_inc, p_inc)))
    }
)

df.index = df.index + n_pulled + 1
df['p_0'] = 1 - df['p_1']

df['p'] = df['p_0'].cumprod().shift(1).fillna(1) * df['p_1']

df['p_cum'] = df['p'].cumsum()

expectation = np.sum(df.index * df['p'])
print(f'Expected pulls needed: {expectation: .2f}')
print(f'Expected pulls remaining: {(expectation-n_pulled): .2f}')


# from matplotlib import pyplot as plt

# plt.plot(df.index.values, df['p_cum'].values)
# plt.title('Cumulative probability')
# plt.show()
