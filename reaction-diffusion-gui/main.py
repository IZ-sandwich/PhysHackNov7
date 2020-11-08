import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QSlider, QLabel
from PyQt5.QtWidgets import QGroupBox, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QTimer

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import scipy.stats as st
import random
from math import floor

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Main Layout
        main_layout = QGridLayout()

        # feed rate
        feedrate_label = QLabel("Feed Rate")
        feedrate_slider = QSlider(Qt.Horizontal)
        feedrate_slider.setRange(0,100)
        feedrate_slider.setValue(55)
        self.feedrate_slider = feedrate_slider

        feedrate_layout = QHBoxLayout()
        feedrate_layout.addWidget(feedrate_label)
        feedrate_layout.addWidget(feedrate_slider)

        # kill rate 
        killrate_label = QLabel("Kill Rate")
        killrate_slider = QSlider(Qt.Horizontal)
        killrate_slider.setRange(0,100)
        killrate_slider.setValue(63)
        self.killrate_slider = killrate_slider
        
        killrate_layout = QHBoxLayout()
        killrate_layout.addWidget(killrate_label)
        killrate_layout.addWidget(killrate_slider)

        # Run Button
        run_button = QPushButton("Run")
        run_button.clicked.connect(self.runButtonClicked)

        # Width, height
        width_label = QLabel("Width")
        width_textbox = QLineEdit()
        width_textbox.setText("100")
        self.width_textbox = width_textbox
        height_label = QLabel("Height")
        height_textbox = QLineEdit()
        height_textbox.setText("100")
        self.height_textbox = height_textbox

        wh_layout = QHBoxLayout()
        wh_layout.addWidget(width_label)
        wh_layout.addWidget(width_textbox)
        wh_layout.addWidget(height_label)
        wh_layout.addWidget(height_textbox)

        layout = QVBoxLayout()
        layout.addLayout(feedrate_layout)
        layout.addLayout(killrate_layout)
        layout.addLayout(wh_layout)
        layout.addWidget(run_button)

        groupBox = QGroupBox("Model Parameters")
        groupBox.setLayout(layout)
        
        self.mpl_canvas = MplCanvas(self, width=1, height=4, dpi=100)
        # A = np.ones((100,100))*255
        # A[50:70,50:70] = 0
        # self.mpl_canvas.axes.imshow(A)

        self.timer = QTimer()
        self.timer.setInterval(100)

        main_layout.addWidget(groupBox,0,0)
        main_layout.addWidget(self.mpl_canvas)

        self.setLayout(main_layout)
        self.resize(600,700)
        self.setWindowTitle("Reaction-Diffusion")

    def runButtonClicked(self):
        feedrate = self.feedrate_slider.value()/1000.0
        killrate = self.killrate_slider.value()/1000.0
        print("{}, {}".format(feedrate, killrate))

        width = int(self.width_textbox.text())
        height = int(self.height_textbox.text())

        self.reaction_diffusion = ReactionDiffusion(feedrate, killrate, (height,width), self.timer, self.mpl_canvas)
        self.timer.start()
        self.timer.timeout.connect(self.reaction_diffusion.iterate)
    
class ReactionDiffusion():
    def __init__(self, feedrate, killrate, dim, timer, mpl_canvas):
        self.dim = dim

        # Defining the Laplacian
        self.laplacian = np.array([[0.05,0.2,0.05],[0.2,-1,0.2],[0.05,0.2,0.05]])

        self.numSteps = 100
        self.stepsPerFrame = 50

        self.timer = timer # For stopping the timer when iterations are finished
        self.stepCount = 0
        self.mpl_canvas = mpl_canvas
        self.plot_ref = None

        # Define Constants
        self.d_a, self.d_b = 1.0, 0.5
        self.f = feedrate 
        self.k = killrate 
        self.step = 1.0

        self.A = np.ones(self.dim)
        self.B = np.zeros(self.dim)

        # Random Seed Points 
        num_seeds = 5
        min_blob = 5
        max_blob = 20

        for _ in range(num_seeds):
            x = random.randint(0, self.dim[1])
            y = random.randint(0, self.dim[0])
            d_x = random.randint(min_blob, max_blob)
            d_y = random.randint(min_blob, max_blob)
            self.B[x - floor(d_x/2): x + floor(d_x/2), y - floor(d_y/2): y + floor(d_y/2)] = 1

        if self.plot_ref is None:
            plot_refs = self.mpl_canvas.axes.imshow((self.A/(self.A+self.B))*255.0)
            self.plot_ref = plot_refs 
        self.mpl_canvas.draw()

    def iterate(self):
        def getF():
            #return (np.ones((len_X, 1)) * np.linspace(0.006, 0.06, len_X)).T
            return self.f

        def getK():
            #return np.ones((len_Y, 1)) * np.linspace(0.050, 0.07, len_Y)
            return self.k

        def getD_B():
            #return 0.5 - gkern(len_X, 3)*2000
            return self.d_b

        def simulationTick():
            A_lp = signal.convolve2d(self.A, self.laplacian, mode='same', boundary='wrap')
            B_lp = signal.convolve2d(self.B, self.laplacian, mode='same', boundary='wrap')

            self.A = self.A + (self.d_a * A_lp - self.A * np.power(self.B, 2) + getF() * (1 - self.A)) * self.step
            self.B = self.B + (getD_B() * B_lp + self.A * np.power(self.B, 2) - (getK() + getF()) * self.B) * self.step

        for _ in range(self.stepsPerFrame):
            simulationTick()
        img = (self.A / (self.A + self.B)) * 255.0

        self.plot_ref.set_array(img)
        self.mpl_canvas.draw()

        self.stepCount += 1
        if (self.stepCount > self.numSteps):
            self.timer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Specifying window parameters
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())