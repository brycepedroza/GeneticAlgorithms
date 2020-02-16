from genetic_alogithm.richardson import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


TEST_PERSON = {'x': {'expend': 0.00441035200695196, 'econ_rest': 0.7853611899007149, 'k_self': 0.7853611899007149, 'k_others': 0.15614796345045187, 'dominant': False, 'curr': 0.7853612081411065}, 'y': {'expend': 0.08843316988617403, 'econ_rest': 0.9350997658890982, 'k_self': 0.8225676762722613, 'k_others': 0.7460931304056792, 'dominant': True, 'curr': 0.9350997658890982}, 'z': {'expend': 0.14908505879026315, 'econ_rest': 0.1487123461432875, 'k_self': 0.004000319280682051, 'k_others': 0.003990318482480346, 'dominant': False, 'curr': 0.14973865760205343}}
NUM_GENERATIONS = 100
NORMALIZE = True

x = Country(**TEST_PERSON['x'])
y = Country(**TEST_PERSON['y'])
z = Country(**TEST_PERSON['z'])
r = Richardson(new=False, x=x, y=y, z=z, normalize=NORMALIZE)


# Lets study how these params work over time.
x_no_reset = []
y_no_reset = []
z_no_reset = []
fitness_no_reset = []

# We will only consider the fittest individual in the calculation
for x in range(NUM_GENERATIONS):
    x_no_reset.append(r.x.curr)
    y_no_reset.append(r.y.curr)
    z_no_reset.append(r.z.curr)
    fitness_no_reset.append(r.fitness)
    r.perform_calculations()

# reset current spending so only 12 params remain.
r.reset_current_spending()
x_reset = []
y_reset = []
z_reset = []
fitness_reset = []
for x in range(NUM_GENERATIONS):
    x_reset.append(r.x.curr)
    y_reset.append(r.y.curr)
    z_reset.append(r.z.curr)
    fitness_reset.append(r.fitness)
    r.perform_calculations()

# Let's calculate how far off the lines are from eventually coming to a steady state.
x_nrmsd = np.sqrt(
    np.mean((np.array(x_reset) - np.array(x_no_reset))) ** 2) \
    / (np.max(x_no_reset))
y_nrmsd = np.sqrt(
    np.mean((np.array(y_reset) - np.array(y_no_reset))) ** 2) \
    / (np.max(y_no_reset))
z_nrmsd = np.sqrt(
    np.mean((np.array(z_reset) - np.array(z_no_reset))) ** 2) \
    / (np.max(z_no_reset))
fitness_nrmsd = np.sqrt(
    np.mean((np.array(fitness_reset) - np.array(fitness_no_reset))) ** 2) \
    / (np.max(fitness_reset))

# The larger the ssd, the worse the result
country_nrmsd = (x_nrmsd + y_nrmsd + z_nrmsd)/3

print(f"{country_nrmsd},{fitness_nrmsd}")

df = pd.DataFrame({'domain': range(NUM_GENERATIONS),
                   'X without Reset': x_no_reset,
                   'Y without Reset': y_no_reset,
                   'Z without Reset': z_no_reset,
                   'X with Reset': x_reset,
                   'Y with Reset': y_reset,
                   'Z with Reset': z_reset})

# multiple line plot
plt.plot('domain', 'X without Reset', data=df, marker='', color='blue', linewidth=2, linestyle='dotted')
plt.plot('domain', 'Y without Reset', data=df, marker='', color='red', linewidth=2, linestyle='dotted')
plt.plot('domain', 'Z without Reset', data=df, marker='', color='green', linewidth=2, linestyle='dotted')
plt.plot('domain', 'X with Reset', data=df, marker='', color='blue', linewidth=2)
plt.plot('domain', 'Y with Reset', data=df, marker='', color='red', linewidth=2)
plt.plot('domain', 'Z with Reset', data=df, marker='', color='green', linewidth=2)

plt.legend()

plt.show(block=True)