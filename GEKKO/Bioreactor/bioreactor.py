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
o2_data = data_file[:, 3]
co2_data = data_file[:, 4]

# GEKKO model init
m = GEKKO(remote=False)
m.time = time

# parameters
rf = m.FV(value=0.5, lb=0, name='R_F (?)'); rf.STATUS = 1
rsmax = m.FV(value=0.01519, lb=0, name='rs_max (%/g-d)'); rsmax.STATUS = 1
ks = m.FV(value=0.186, lb=0); ks.STATUS = 1
yxs = m.FV(value=5.60, lb=0); yxs.STATUS = 1
mum = m.FV(value=0.118, lb=0, name='mu_maintenance (1/d)'); mum.STATUS = 1
romax = m.FV(value=85, lb=0, name="ro_max (%/g-d)"); romax.STATUS = 1
ko = m.FV(value= 6.32, lb=0, name="k_o (%)"); ko.STATUS = 1
osat = m.FV(value= 86.2, lb=0, name="o_sat (%)"); osat.STATUS = 1
kL = m.FV(value= 0.0137, lb=0, name="k_L (h/L-d)"); kL.STATUS = 1
yco = m.FV(value=0.897, lb=0); yxs.STATUS = 1
vL = m.FV(value=0.05); vL.STATUS = 1

# variables
rs = m.CV(); rs.FSTATUS = 1
mu = m.CV(); mu.FSTATUS = 1
ro = m.CV(); ro.FSTATUS = 1
rc = m.CV(); rc.FSTATUS = 1
s = m.CV(value=substrate_data, lb=0); s.FSTATUS = 1
x = m.CV(value=cells_data, lb=0); x.FSTATUS = 1
o = m.CV(value=o2_data, lb=0); o.FSTATUS = 1
c = m.CV(value=co2_data, lb=0); c.FSTATUS = 1

# intermediate equations
m.Equation(rs == rsmax * s / (ks + s))
m.Equation(mu == yxs * rs - mum)
m.Equation(ro == romax * o / (osat + o))
m.Equation(rc == yco * ro)

# dynamic equations
m.Equation(s.dt() == -rs * x + rf)
m.Equation(x.dt() == mu * x)
m.Equation(ro * x == (osat - o) * kL * vL)
m.Equation(c == rc * x / vL)

# regression mode
m.options.IMODE = 5  # dynamic estimation
m.options.NODES = 5  # collocation nodes
m.options.EV_TYPE = 2  # squared error
m.solve(disp=True)  # display solver output

# print regressed parameters
print(
  'rsmax = ' + str(rsmax.value[0]) + '\n'
  + 'ks = ' + str(ks.value[0]) + '\n'
  + 'yxs = ' + str(yxs.value[0]) + '\n'
  + 'mum = ' + str(mum.value[0]) + '\n'
)

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

# cells model curve 
ax1.plot(time, x, color=color, marker='None')

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
