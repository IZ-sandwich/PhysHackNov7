import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.stats as st
import random
from math import floor
from matplotlib import animation, rc
from IPython.display import HTML

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class ReactionDiffusion(FigureCanvasQTAgg):
    def __init__(self, width=5, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvasQTAgg.__init__(self, self.fig)
        super(ReactionDiffusion, self).__init__(self.fig)


    def run(self, feedrate, killrate):
        # Defining the Laplacian
        laplacian = np.array([[0.05,0.2,0.05],[0.2,-1,0.2],[0.05,0.2,0.05]])

        len_X, len_Y = 500, 500
        dim = (len_X,len_Y)

        showAnimation = True
        numSteps = 100
        stepsPerFrame = 100

        # Define Constants
        d_a, d_b = 1.0, 0.5
        f = feedrate 
        k = killrate 
        step = 1.0

        A = np.ones(dim)
        B = np.zeros(dim)

        # Random Seed Points 
        num_seeds = 5
        min_blob = 5
        max_blob = 20

        for _ in range(num_seeds):
            x = random.randint(0, len_X)
            y = random.randint(0, len_Y)
            d_x = random.randint(min_blob, max_blob)
            d_y = random.randint(min_blob, max_blob)
            B[x - floor(d_x/2): x + floor(d_x/2), y - floor(d_y/2): y + floor(d_y/2)] = 1

        # def gkern(kernlen=21, nsig=3):
        #     """Returns a 2D Gaussian kernel."""

        #     x = np.linspace(-nsig, nsig, kernlen+1)
        #     kern1d = np.diff(st.norm.cdf(x))
        #     kern2d = np.outer(kern1d, kern1d)
        #     return kern2d/kern2d.sum()

        def getF():
            #return (np.ones((len_X, 1)) * np.linspace(0.006, 0.06, len_X)).T
            return f

        def getK():
            #return np.ones((len_Y, 1)) * np.linspace(0.050, 0.07, len_Y)
            return k

        def getD_B():
            #return 0.5 - gkern(len_X, 3)*2000
            return d_b

        # def initPlot():
        #     print('hi really')
        #     pos.set_array(A)
        #     return pos,

        def simulationTick(A,B):
            A_lp = signal.convolve2d(A, laplacian, mode='same')#, boundary='wrap')
            B_lp = signal.convolve2d(B, laplacian, mode='same')#, boundary='wrap')

            A = A + (d_a * A_lp - A * np.power(B, 2) + getF() * (1 - A)) * step
            B = B + (getD_B() * B_lp + A * np.power(B, 2) - (getK() + getF()) * B) * step

        # def updatePlot(i):
        #     print('byby')
        #     print(i)
        #     global A
        #     global B
        #     for _ in range(stepsPerFrame):
        #         simulationTick()
        #     img = (A / (A + B)) * 255.0
        #     pos.set_array(img)
        #     return pos,

        # if not showAnimation:
        #     for i in range(numSteps * stepsPerFrame):
        #         simulationTick()

        for _ in range(numSteps):
            for _ in range(stepsPerFrame):
                simulationTick(A,B)
            img = (A / (A + B)) * 255.0
            self.axes.cla() 
            self.axes.imshow(img)
            self.draw()
        #     plt.show()
        # img = (A / (A + B)) * 255.0
        # pos = self.axes.imshow(img)
        # plt.show()

        # if showAnimation:
        #     anim = animation.FuncAnimation(self.fig, updatePlot, frames=numSteps, init_func=initPlot, blit=True)
        #     print('wowow')
        # HTML(anim.to_html5_video())
