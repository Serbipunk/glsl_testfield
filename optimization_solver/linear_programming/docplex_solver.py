from docplex.mp.model import Model
m = Model(name='linear_programming_example')

# variables
foldyphone = m.continuous_var(name='foldyphone')
tinyphone = m.continuous_var(name='tinyphone')

foldyphonetime = 1.5
tinyphonetime = 2

# constraints
foldyphoneprod = m.add_constraint(foldyphone >= 500)
tinyphoneprod = m.add_constraint(tinyphone >= 200)
totalprod = m.add_constraint(m.sum([tinyphone*tinyphonetime, foldyphone*foldyphonetime]) <= 2999.5)

# goals
m.maximize(foldyphone*900 + tinyphone*1100)

# solution
sol = m.solve()
sol.display()

