from scipy.optimize import minimize
import matplotlib.pyplot as plt
import numpy as np

#Define objective function
def objective_function(x):
    return 0.5 * x @ Q @ x + p @ x

#Define constraints
def constraint(x):
    return G @ x - h

#Define optimization
#Problem data
#Quadratic weight coefficients
Q = np.array([[1, 0], [0, 2]])
#Linear weight coefficients
p = np.array([1, 2])
#Strength coefficients
G = np.array([[1, 1], [1, 2], [2, 1]])
#Strength constraints
h = np.array([3, 4, 5])
#Initial guess
x0 = np.array([0, 0])

con = {'type': 'ineq', 'fun': constraint}
b = (0,10); bnds = (b,b)
opt = {'maxiter':1000}
res = minimize(objective_function, x0,
               constraints=con, bounds=bnds,
               method='SLSQP', options=opt)

#print results
print(f'Optimal solution: x = {res.x}')
print(f'Minimum weight = {res.fun}')
