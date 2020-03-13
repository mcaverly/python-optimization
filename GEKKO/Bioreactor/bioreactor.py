from gekko import GEKKO
import numpy as np
import matplotlib.pyplot as plt
'''
Cultivation of isolated plant cells in suspension culture (adapted from APMonitor example for Cell Cultrure). Only cell and substrate are considered (product is the cells in this process). A set of hypothetical experimental data is used to fit theoretical model to experiment.

Munack A., Posten C. (1989): Design of optimal dynamical experiments for parameter estimation, Proceedings of the Americal Control Conference, Vol. 4, 2010-2016. 
'''
#
# Data init
#
data_file = np.loadtxt('GEKKO/Bioreactor/data.txt', delimiter=',')
time = data_file[:, 0]
cells_data = data_file[:, 1]
substrate_data = data_file[:, 2]

# GEKKO model init
m = GEKKO(remote=False)
m.time = time #np.linspace(0,20,nt)

# parameters
rsmax = m.FV(value=0.05, lb=0); rsmax.STATUS = 1 
ks = m.FV(value=0.2, lb=0); ks.STATUS = 1  
x = m.FV(value=cells_data)

# variables
s = m.CV(value=substrate_data); s.FSTATUS = 1

# regression equation
m.Equation(s.dt() == -rsmax * (s * x / (ks + s)))

# regression mode
m.options.IMODE = 5   # dynamic estimation
m.options.NODES = 5   # collocation nodes
m.options.EV_TYPE = 2 # squared error
m.solve(disp=True)    # display solver output

# print parameters
print('Optimized, rsmax = ' + str(rsmax.value[0]) + ' ks = ' +
      str(ks.value[0]))

#
# Plot curve(s)
#
fig, ax1 = plt.subplots()

color = 'tab:red'
marker = 'x'
ax1.set_xlabel('Time (days)')
ax1.set_ylabel('Biomass (g/L)', color=color)
ax1.plot(time, cells_data, color=color, marker=marker, linestyle='None')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
marker = '.'
ax2.set_ylabel(
    'Substrate (%)', color=color)  # we already handled the x-label with ax1
ax2.plot(time, substrate_data, color=color, marker=marker, linestyle='None')
ax2.tick_params(axis='y', labelcolor=color)

# substrate model curve
ax2.plot(time, s, color=color, marker='None')

fig.tight_layout()  # otherwise the right y-label is slightly clipped

# save output (required for Repl.it)
plt.savefig('GEKKO/Bioreactor/model_plot.png')