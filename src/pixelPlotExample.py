import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as cm2

L = 10
N = 100

x = np.linspace(0, L, N)
y = np.linspace(0, L, N)
temp = x * y
A = np.zeros((N, N))
for col in range(N):
    for row in range(N):
        A[col, row] = col * row

# nrows, ncols = 100, 100
# grid = temp.reshape((nrows, ncols))

# plt.pcolor(temp, extent=(x.min(), x.max(), y.max(), y.min()),
#            interpolation='nearest', cmap=cm.jet)

plt.pcolor(A, cmap="rainbow")

plt.show()
