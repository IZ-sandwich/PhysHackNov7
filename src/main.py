import random
from math import floor

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.stats as st
from matplotlib import animation, rc
# from IPython.display import HTML

laplacian = np.array([[0.05, 0.2, 0.05], [0.2, -1, 0.2], [0.05, 0.2, 0.05]])
len_X = 200
len_Y = 200

dim = (len_X,len_Y)

showAnimation = False
numSteps = 800
stepsPerFrame = 100

# Diffusion Rates
d_a = 0.82
d_b = 0.5
f = 0.055
k = 0.062
step = 1.0

A = np.ones(dim)
B = np.zeros(dim)

# Seeding
# B[70:80,80:85] = 1
# B[50:55,50:55] = 1
# B[60:80,80:85] = 1

# Random blobs
num_seeds = 5
min_blob = 5
max_blob = 20

for i in range(num_seeds):
  x = random.randint(0, len_X)
  y = random.randint(0, len_Y)
  d_x = random.randint(min_blob, max_blob)
  d_y = random.randint(min_blob, max_blob)
  B[x - floor(d_x/2): x + floor(d_x/2), y - floor(d_y/2): y + floor(d_y/2)] = 1

def gkern(kernlen=21, nsig=3):
  """Returns a 2D Gaussian kernel."""

  x = np.linspace(-nsig, nsig, kernlen + 1)
  kern1d = np.diff(st.norm.cdf(x))
  kern2d = np.outer(kern1d, kern1d)
  return kern2d / kern2d.sum()

def initPlot():
  pos.set_array(A)
  return pos,

def simulationTick():
  global A
  global B
  A_lp = signal.convolve2d(A, laplacian, mode='same')
  B_lp = signal.convolve2d(B, laplacian, mode='same')

  A = A + (d_a * A_lp - A * np.power(B, 2) + f * (1 - A)) * step
  B = B + (d_b * B_lp + A * np.power(B, 2) - (k + f) * B) * step

def updatePlot(frame):
  global A
  global B
  for i in range(stepsPerFrame):
    simulationTick()
  img = (A / (A + B)) * 255.0
  pos.set_array(img)
  return pos,

if not showAnimation:
  for i in range(numSteps * stepsPerFrame):
    simulationTick()

plt.show()

# print(A)
# print(B)
img = (A / (A + B)) * 255.0

fig, (ax1) = plt.subplots(figsize=(10, 10))
pos = ax1.imshow(img)
fig.colorbar(pos, ax=ax1)
np.sum(B)

if showAnimation:
  anim = animation.FuncAnimation(fig, updatePlot, frames=numSteps,
                                 init_func=initPlot, blit=True)
  # HTML(anim.to_html5_video())

plt.show()
