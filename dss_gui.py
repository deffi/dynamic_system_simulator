#!/usr/bin/env python

from __future__ import unicode_literals
import sys, random
from PySide import QtGui, QtCore

import matplotlib
matplotlib.rcParams['backend.qt4']='PySide'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MplWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)

        # Required? Can we access it in another way?
        self.fig=fig
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.updateGeometry()
        self.fig.tight_layout()

    def plot(self, *args, **kwargs):
        self.axes.plot(*args, **kwargs)
        self.draw()

    def resizeEvent(self, event):
        super(MplWidget, self).resizeEvent(event)
        self.fig.tight_layout()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        central_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(central_widget)
        dc = MplWidget(central_widget, width=5, height=4, dpi=100)
        self._dc=dc
        l.addWidget(dc)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(250)

        central_widget.setFocus()
        self.setCentralWidget(central_widget)

    def update_figure(self):
        x = [0, 1, 2, 3]
        y = [ random.randint(0, 10) for _ in range(4) ]
        self._dc.plot(x, y, 'r')

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()


app = QtGui.QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Dynamic System Simulator")
window.show()
sys.exit(app.exec_())
