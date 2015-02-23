#!/usr/bin/env python

from __future__ import unicode_literals
import sys
import traceback

from PySide import QtGui, QtCore

import numpy as np

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
        #self.axes.hold(False)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.updateGeometry()
        self.fig.tight_layout()

    def clear(self):
        self.axes.clear()

    def plot(self, *args, **kwargs):
        self.axes.plot(*args, **kwargs)
        self.draw()
        self.fig.tight_layout()

    def resizeEvent(self, event):
        # Seems like we have to call super before and after the call to
        # tight_layout; if either is skipped, it does not work correctly when
        # the containing window is maximized.
        super(MplWidget, self).resizeEvent(event)
        self.fig.tight_layout()
        super(MplWidget, self).resizeEvent(event)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        central_widget = QtGui.QWidget(self)
        parameters_pane = QtGui.QWidget(central_widget)
        self._plotWidget = MplWidget(central_widget, width=5, height=4, dpi=100)

        self._exceptionWidget = QtGui.QTextEdit(central_widget)
        self._exceptionWidget.setReadOnly(True)

        mass_label = QtGui.QLabel("&Mass:", parameters_pane)
        self._mass_input = QtGui.QDoubleSpinBox(parameters_pane)
        self._mass_input.setSuffix(" kg")
        self._mass_input.setRange(sys.float_info.min, sys.float_info.max)
        self._mass_input.setDecimals(1)
        self._mass_input.setSingleStep(0.1)
        self._mass_input.setValue(0.5)
        self._mass_input.valueChanged.connect(self.simulate)
        mass_label.setBuddy(self._mass_input)
        
        stiffness_label = QtGui.QLabel("&Stiffness:", parameters_pane)
        self._stiffness_input = QtGui.QDoubleSpinBox(parameters_pane)
        self._stiffness_input.setSuffix(" N/m")
        self._stiffness_input.setRange(sys.float_info.min, sys.float_info.max)
        self._stiffness_input.setDecimals(1)
        self._stiffness_input.setSingleStep(0.1)
        self._stiffness_input.setValue(1.5)
        self._stiffness_input.valueChanged.connect(self.simulate)
        stiffness_label.setBuddy(self._stiffness_input)
        
        central_widget_layout = QtGui.QVBoxLayout(central_widget)
        central_widget_layout.setContentsMargins(0, 0, 0, 0)
        central_widget_layout.setSpacing(0)
        central_widget_layout.addWidget(parameters_pane)
        central_widget_layout.addWidget(self._plotWidget)
        central_widget_layout.addWidget(self._exceptionWidget)
        
        parameters_pane_layout = QtGui.QGridLayout(parameters_pane)
        parameters_pane_layout.addWidget(mass_label, 0, 0)
        parameters_pane_layout.addWidget(self._mass_input, 0, 1)
        parameters_pane_layout.addWidget(stiffness_label, 1, 0)
        parameters_pane_layout.addWidget(self._stiffness_input, 1, 1)
        parameters_pane_layout.setColumnStretch(2, 1)

        self._mass_input.setFocus()
        self.setCentralWidget(central_widget)

        self.simulate()
        
    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def simulate(self):
        try:
            self._exceptionWidget.setText("")
            
            from systems import Pendulum
    
            pendulum = Pendulum()
            pendulum.spring.stiffness.set(round(self._stiffness_input.value(), 5))
            pendulum.mass.mass       .set(round(self._mass_input.value(), 5))
            # It should be irrelevant which one we assign to, because it's the same variable
            pendulum.mass.position.set(1)
            #pendulum.spring.displacement = 1
    
            t = np.arange(0, 10, 0.1)
            x = np.zeros(np.size(t))
    
            for i in range(len(t)):
                x[i] = pendulum.mass.position.get()
    
                dt = t[i]-t[i-1] if i>0 else None
                pendulum.update(t[i], dt)
    
            self._plotWidget.clear()
            self._plotWidget.plot(t, x)

            self._exceptionWidget.hide()
            self._plotWidget.show()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            s="".join(traceback.format_exception(exc_type, exc_value, exc_traceback, chain=True))
            self._exceptionWidget.setText(s)

            self._exceptionWidget.show()
            self._plotWidget.hide()

app = QtGui.QApplication(sys.argv)

window = MainWindow()
window.setWindowTitle("Dynamic System Simulator")
window.show()
sys.exit(app.exec_())
