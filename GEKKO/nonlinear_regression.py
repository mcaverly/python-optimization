from gekko import GEKKO
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# measurements
xm = np.array([0, 1, 2, 3, 4, 5])
ym = np.array([0.1, 0.2, 0.3, 0.5, 0.8, 2.0])

# GEKKO model
m = GEKKO()

# parameters
x = m.Param(value=xm)
a = m.FV(value=0.1)  # initial guess at parameter value
a.status = 1  # let solver fit value of parameter a
b = m.FV(value=0.1)  # initial guess at parameter value
b.status = 1  # let solver fit value of parameter a

# variables
y = m.CV(value=ym)
y.FSTATUS = 1  # let solver use the values of y in solution

# regression equation
m.Equation(y == a * m.exp(b * x))

# regression mode
m.options.EV_TYPE = 2  # sum squared errors
m.options.IMODE = 2  # steady-state model parameter update (MPU)

# optimize
m.solve()  # pass parameter "disp=False" to hide solver outlet

# print parameters
print('Optimized, a = ' + str(a.value[0]) + ' b = ' + str(b.value[0]))

plt.plot(xm, ym, 'bo')
plt.plot(xm, y.value, 'r-')
plt.savefig('GEKKO/nonlinear_regression_plot.png')
