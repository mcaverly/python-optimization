from gekko import GEKKO
'''
Mixed Integer Nonlinear Programming 

Example #10 from APMonitor.com
http://apmonitor.com/wiki/index.php/Main/GekkoPythonOptimization
'''

m = GEKKO()
m.options.SOLVER = 1  # APOPT is an MINLP solver
# optional solver settings with APOPT
m.solver_options = ['minlp_maximum_iterations 500', \
                    # minlp iterations with integer solution

                    'minlp_max_iter_with_int_sol 10', \
                    # treat minlp as nlp

                    'minlp_as_nlp 0', \
                    # nlp sub-problem max iterations

                    'nlp_maximum_iterations 50', \
                    # 1 = depth first, 2 = breadth first

                    'minlp_branch_method 1', \
                    # maximum deviation from whole number

                    'minlp_integer_tol 0.05', \
                    # covergence tolerance

                    'minlp_gap_tol 0.01']

# initialize variables
x1 = m.Var(value=1, lb=1, ub=5)
x2 = m.Var(value=5, lb=1, ub=5)
x3 = m.Var(value=5, lb=1, ub=5, integer=True)
x4 = m.Var(value=1, lb=1, ub=5, integer=True)

# constraint and objective equations
m.Equation(x1 * x2 * x3 * x4 >= 25)
m.Equation(x1**2 + x2**2 + x3**2 + x4**2 == 40)
m.Obj(x1 * x4 * (x1 + x2 + x3) + x3)

# solve
m.solve()

# output solution
print(x1.value, x2.value, x3.value, x4.value)
