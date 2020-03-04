from gekko import GEKKO
import numpy as np

# initialize model
m = GEKKO()

#help(m)

# define parameter
eq = m.Param(value=40)

# initialize variables
x1 = m.Var(value=1,lb=1,ub=5)
x2 = m.Var(value=5,lb=1,ub=5)
x3 = m.Var(value=5,lb=1,ub=5)
x4 = m.Var(value=1,lb=1,ub=5)

# equations
m.Equation(x1 * x2 * x3 * x4 >= 25)
m.Equation(x1**2 + x2**2 + x3**2 + x4**2 == eq)

# objective
m.Obj(x1 * x4 * (x1 + x2 + x3) + x3)

# set global options
m.options.IMODE = 3  # steady state optimization
m.options.SOLVER = 3 # IPOPT solver

# solve simulation
m.solve()

#Results
print('')
print('Results')
print('x1: ' + str(x1.value))
print('x2: ' + str(x2.value))
print('x3: ' + str(x3.value))
print('x4: ' + str(x4.value))