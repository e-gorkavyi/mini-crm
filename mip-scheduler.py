from itertools import product
from mip import Model, BINARY

n = 20
m = 3

times = [[15, 7, 21],
         [12, 4, 30],
         [3, 28, 18],
         [12, 4, 30],
         [32, 2, 10],
         [15, 7, 21],
         [15, 7, 21],
         [12, 4, 30],
         [3, 28, 18],
         [12, 4, 30],
         [32, 2, 10],
         [15, 7, 21],
         [15, 7, 21],
         [12, 4, 30],
         [3, 28, 18],
         [12, 4, 30],
         [32, 2, 10],
         [15, 7, 21],
         [3, 28, 18],
         [12, 4, 30]]

for i in range(n):
	for j in range(m):
		print(i, j)

M = sum(times[i][j] for i in range(n) for j in range(m))

machines = [[0, 1, 2],
            [1, 0, 2],
            [2, 1, 0],
            [0, 1, 2],
            [1, 0, 2],
            [2, 1, 0],
            [0, 1, 2],
            [1, 0, 2],
            [2, 1, 0],
            [0, 1, 2],
            [1, 0, 2],
            [2, 1, 0],
            [2, 1, 0],
            [0, 1, 2],
            [1, 0, 2],
            [2, 1, 0],
            [0, 1, 2],
            [1, 0, 2],
            [2, 1, 0],
            [0, 1, 2]]

model = Model('JSSP')

c = model.add_var(name="C")
x = [[model.add_var(name='x({},{})'.format(j + 1, i + 1))
      for i in range(m)] for j in range(n)]
y = [[[model.add_var(var_type=BINARY, name='y({},{},{})'.format(j + 1, k + 1, i + 1))
       for i in range(m)] for k in range(n)] for j in range(n)]

model.objective = c

for (j, i) in product(range(n), range(1, m)):
	model += x[j][machines[j][i]] - x[j][machines[j][i - 1]] >= times[j][machines[j][i - 1]]

for (j, k) in product(range(n), range(n)):
	if k != j:
		for i in range(m):
			model += x[j][i] - x[k][i] + M * y[j][k][i] >= times[k][i]
			model += -x[j][i] + x[k][i] - M * y[j][k][i] >= times[j][i] - M

for j in range(n):
	model += c - x[j][machines[j][m - 1]] >= times[j][machines[j][m - 1]]

model.optimize(max_seconds=30)

print("\n\nCompletion time: ", c.x)
for (j, i) in product(range(n), range(m)):
	print("task %d starts on machine %d at time %g " % (j + 1, i + 1, x[j][i].x))
