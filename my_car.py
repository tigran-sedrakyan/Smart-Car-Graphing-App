import sys
from PyQt4.QtGui import *
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from decimal import *

class Plot(pg.PlotWidget):

	def __init__(self):
		super(Plot, self).__init__()

		pg.setConfigOptions(antialias=True)

		self.setTitle('Acceleration-distance dependency graph')
		self.enableAutoRange('y', 1)
		self.enableAutoRange('x', 1)
		self.showGrid(x=True, y=True)

		self.label = QLabel()
		self.proxy = pg.SignalProxy(self.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)


		self.l0 = self.getPlotItem().addLine(x = 0, movable = False, pen = {'color': "w"})
		self.l1 = self.getPlotItem().addLine(y = 0, movable = False, pen = {'color': "w"})	
		self.l2 = self.plot()
		self.l3 = self.plot()
		self.l4 = self.plot()
		self.l5 = self.plot()
		
		self.distance = 0
		self.length = 0
		self.t_yellow = 0
		self.v_0 = 0
		self.v_limit = 0
		self.a_max = 0
		self.a_min = 0

		self.getPlotItem().setLabel('left', text = 'Distance (m)')
		self.getPlotItem().setLabel('bottom', text = 'Acceleration (m/s^2)')
		
	def set_distance(self, D):
		self.distance = float(D)

	def set_length(self, L):
		self.length = float(L)

	def set_t_yellow(self, time):
		self.t_yellow = float(time)

	def set_v_0(self, velocity):
		self.v_0 = float(velocity)*1000/float(3600)
	
	def set_v_limit(self, v_limit):
		self.v_limit = float(v_limit)*1000/float(3600)

	def set_a_max(self, acceleration):
		self.a_max = float(acceleration)

	def set_a_min(self, acceleration):
		if (float(acceleration) < 0):
			self.a_min = float(acceleration)
		else:
			self.a_min = -float(acceleration)

	def update_plot(self):
		
		#Default axes

		l0 = self.getPlotItem().addLine(x = 0, movable = False, pen = {'color': "w"})
		l1 = self.getPlotItem().addLine(y = 0, movable = False, pen = {'color': "w"})

		#Some infinite lines

		if self.distance != 0:
			l2 = self.getPlotItem().addLine(y = self.distance, movable = True, pen = "r")
		else:
			pass

		if self.length != 0:	
			l3 = self.getPlotItem().addLine(y = self.length+self.distance, movable = True, pen = "g")
		else:
			pass

		if self.a_min != 0:
			l4 = self.getPlotItem().addLine(x = self.a_min, movable = False, pen = {'color': "m"})
		else:
			pass

		if self.a_max != 0:
			l5 = self.getPlotItem().addLine(x = self.a_max, movable = False, pen = {'color': "c"})
		else:
			pass


		#Graph in case of acceleration

		r1 = int(100*self.a_max)+1
		A_max = np.empty([r1, ])
		Accel_distance = np.empty([r1, ])
		a_max = 0
		for i in range(0, r1):
			A_max[i] = a_max
			if a_max == 0:
				Accel_distance[0] = self.v_0*self.t_yellow
			else:
				if self.v_0 > self.v_limit:
					Accel_distance[i] = self.v_0*self.t_yellow
				else:
					self.t_limit = (self.v_limit - self.v_0)/float(a_max)
					if self.t_limit < self.t_yellow:
						Accel_distance[i] = self.v_0*self.t_limit + a_max*self.t_limit*self.t_limit/float(2) + self.v_limit*(self.t_yellow - self.t_limit)
					else:
						Accel_distance[i] = self.v_0*self.t_yellow + a_max*self.t_yellow*self.t_yellow/float(2)
			a_max = a_max + 1/100


		p1 = self.plot(x = A_max, y = Accel_distance, pen = 'b')

		#Graph in case of deceleration

		if self.a_min != 0:
			r2 = int(self.a_min*100)
			A_min = np.empty([-self.a_min*100, ])
			Stop_distance = np.empty([-self.a_min*100, ])
			a_min = 0
			for i in range(r2, 0):
				a_min = a_min - 1/100
				A_min[i] = a_min
				Stop_distance[i] = -self.v_0*self.v_0/float(2*a_min)
		else:
			pass

		try:
			p2 = self.plot(x = A_min, y = Stop_distance, pen = 'y')
		except:
			pass

		#Graphing options

		self.enableAutoRange('y', 0.1)
		self.enableAutoRange('x', 1)

	def set_position_label(self, arg):
		self.label = arg

	def mouseMoved(self, evt):
		mousePoint = self.getPlotItem().vb.mapSceneToView(evt[0])
		self.label.setText("<span style='font-size: 15pt'> Coordinates: a = %0.2f (m/s^2), <span style='font-size: 15pt'> x = %0.2f (m)</span>" % (mousePoint.x(), mousePoint.y()))

class Dialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(Dialog, self).__init__(parent)

		self.setWindowTitle("Coloring and info")
		self.setWindowIcon(QtGui.QIcon('car.png'))

		self.redlabel = QtGui.QLabel("Red")
		self.redlabel.setStyleSheet("QLabel {color : red}")

		self.yellowlabel = QtGui.QLabel("Yellow")
		self.yellowlabel.setStyleSheet("QLabel {color : yellow}")

		self.greenlabel = QtGui.QLabel("Green")
		self.greenlabel.setStyleSheet("QLabel {color : green}")
		
		self.bluelabel = QtGui.QLabel("Blue")
		self.bluelabel.setStyleSheet("QLabel {color : blue}")

		self.violetlabel = QtGui.QLabel("Violet")
		self.violetlabel.setStyleSheet("QLabel {color : darkviolet}")

		self.lightbluelabel = QtGui.QLabel("Light-blue")
		self.lightbluelabel.setStyleSheet("QLabel {color : lightblue}")

		self.whitelabel = QtGui.QLabel("White")
		self.whitelabel.setStyleSheet("QLabel { color : black}")

		self.whitedescription = QtGui.QLabel('Acceleration and Distance axes')
		self.reddescription = QtGui.QLabel('Distance from the intersection(line is movable)')
		self.greendescription = QtGui.QLabel('Distance from the intersection + Length of the intersection (line is movable)')
		self.violetdescription = QtGui.QLabel('Minimum acceleration of the car')
		self.lightbluedescription = QtGui.QLabel('Maximum acceleration of the car')
		self.yellowdescription = QtGui.QLabel('Graph in case of deceleration')
		self.bluedescription = QtGui.QLabel('Graph is case of acceleration')

		self.infolabel = QtGui.QLabel('\n\nYou can use mouse right button in order to make some corrections to the graph.\nAlso you can use mouse scroller (middle button) in order to zoom-in or -out')
		self.aboutlabel =QtGui.QLabel('\n\nTigran Sedrakyan\nAmerican University of Armenia\nSmart Car Graphing App, version 0.2 from 11/29/2016\nAll rights are reserved')
		self.aboutlabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

		self.layout = QtGui.QGridLayout(self)
		self.layout.addWidget(self.whitelabel, 1, 1)
		self.layout.addWidget(self.redlabel, 2, 1)
		self.layout.addWidget(self.greenlabel, 3, 1)
		self.layout.addWidget(self.violetlabel, 4, 1)
		self.layout.addWidget(self.lightbluelabel, 5, 1)
		self.layout.addWidget(self.yellowlabel, 6, 1)
		self.layout.addWidget(self.bluelabel, 7, 1)
		self.layout.addWidget(self.whitedescription, 1, 2)
		self.layout.addWidget(self.reddescription, 2, 2)
		self.layout.addWidget(self.greendescription, 3, 2)
		self.layout.addWidget(self.violetdescription, 4, 2)
		self.layout.addWidget(self.lightbluedescription, 5, 2)
		self.layout.addWidget(self.yellowdescription, 6, 2)
		self.layout.addWidget(self.bluedescription, 7, 2)
		self.layout.addWidget(self.infolabel, 8, 1, 1, 2)
		self.layout.addWidget(self.aboutlabel, 15, 1, 1, 2)


class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()
		
		self.setWindowTitle('Smart Car App')
		self.setWindowIcon(QtGui.QIcon('car.png'))
		
		self.dialog = Dialog()
		plot = Plot()
		
		btn = QtGui.QPushButton("Exit", self)
		btn.clicked.connect(self.close_application)

		btn2 = QtGui.QPushButton("Coloring and info", self)
		btn2.clicked.connect(self.open_dialog)


		timeEdit = QtGui.QLineEdit(self)
		timeEdit.setPlaceholderText('Ty');
		timeEdit.setValidator(QtGui.QDoubleValidator(2.00,4.00, 2))
		timeEdit.textChanged.connect(lambda: plot.clear())
		timeEdit.textChanged.connect(lambda: plot.set_t_yellow(timeEdit.text()))
		timeEdit.textChanged.connect(plot.update_plot)
		timeEdit.textChanged.connect(plot.show)

		a_maxEdit = QtGui.QLineEdit(self)
		a_maxEdit.setPlaceholderText('a_max');
		a_maxEdit.setValidator(QtGui.QDoubleValidator(0.00,3.00, 2))
		a_maxEdit.textChanged.connect(lambda: plot.clear())
		a_maxEdit.textChanged.connect(lambda: plot.set_a_max(a_maxEdit.text()))
		a_maxEdit.textChanged.connect(plot.update_plot)
		a_maxEdit.textChanged.connect(plot.show)

		a_minEdit = QtGui.QLineEdit(self)
		a_minEdit.setPlaceholderText('a_min');
		a_minEdit.setValidator(QtGui.QDoubleValidator(-3.00,0.00, 2))
		a_minEdit.textChanged.connect(lambda: plot.clear())
		a_minEdit.textChanged.connect(lambda: plot.set_a_min(a_minEdit.text()))
		a_minEdit.textChanged.connect(plot.update_plot)
		a_minEdit.textChanged.connect(plot.show)

		v_0Edit = QtGui.QLineEdit(self)
		v_0Edit.setPlaceholderText('V0');
		v_0Edit.setValidator(QtGui.QDoubleValidator(20.00,80.00, 2))
		v_0Edit.textChanged.connect(lambda: plot.clear())
		v_0Edit.textChanged.connect(lambda: plot.set_v_0(v_0Edit.text()))
		v_0Edit.textChanged.connect(plot.update_plot)
		v_0Edit.textChanged.connect(plot.show)

		v_limitEdit = QtGui.QLineEdit(self)
		v_limitEdit.setPlaceholderText('V_limit');
		v_limitEdit.setValidator(QtGui.QDoubleValidator(40.00,90.00, 2))
		v_limitEdit.textChanged.connect(lambda: plot.clear())
		v_limitEdit.textChanged.connect(lambda: plot.set_v_limit(v_limitEdit.text()))
		v_limitEdit.textChanged.connect(plot.update_plot)
		v_limitEdit.textChanged.connect(plot.show)


		distanceEdit = QtGui.QLineEdit(self)
		distanceEdit.setPlaceholderText('D');
		distanceEdit.setValidator(QtGui.QDoubleValidator(7.00,50.00, 2))
		distanceEdit.textChanged.connect(lambda: plot.clear())
		distanceEdit.textChanged.connect(lambda: plot.set_distance(distanceEdit.text()))
		distanceEdit.textChanged.connect(plot.update_plot)
		distanceEdit.textChanged.connect(plot.show)

		lengthEdit = QtGui.QLineEdit(self)
		lengthEdit.setPlaceholderText('L');
		lengthEdit.setValidator(QtGui.QDoubleValidator(7.00,20.00, 2))
		lengthEdit.textChanged.connect(lambda: plot.clear())
		lengthEdit.textChanged.connect(lambda: plot.set_length(lengthEdit.text()))
		lengthEdit.textChanged.connect(plot.update_plot)
		lengthEdit.textChanged.connect(plot.show)

		position_label = QLabel()
		position_label.setText("<span style='font-size: 15pt, '>Coordinates: a=0 (m/s^2),   <span style='', 'font-size: 15pt'>x=0 (m)</span>")
		plot.set_position_label(position_label)

		distanceLabel = QtGui.QLabel('Distance from the intersection (m):')
		lengthLabel = QtGui.QLabel('Length of the intersection (m):')
		a_minLabel = QtGui.QLabel('Minimum acceleration of the car (m/s^2):')
		a_maxLabel = QtGui.QLabel('Maximum acceleration of the car (m/s^2):')
		timeLabel = QtGui.QLabel('Time of the yellow light (s):')
		v_0Label = QtGui.QLabel('Current velocity (km/h):')
		v_limitLabel = QtGui.QLabel('Speed Limit (km/h):')


		layout = QtGui.QGridLayout(self)
		layout.addWidget(distanceLabel, 1, 2)
		layout.addWidget(lengthLabel, 2, 2)
		layout.addWidget(a_maxLabel, 3, 2)
		layout.addWidget(a_minLabel, 4, 2)
		layout.addWidget(timeLabel, 5, 2)
		layout.addWidget(v_0Label, 6, 2)
		layout.addWidget(v_limitLabel, 7, 2)
		
		layout.addWidget(distanceEdit, 1, 3)
		layout.addWidget(lengthEdit, 2, 3)
		layout.addWidget(a_maxEdit, 3, 3)
		layout.addWidget(a_minEdit, 4, 3)
		layout.addWidget(timeEdit, 5, 3)
		layout.addWidget(v_0Edit, 6, 3)
		layout.addWidget(v_limitEdit, 7, 3)
		
		layout.addWidget(btn2, 10, 2, 1, 2)
		layout.addWidget(btn, 11, 2, 1, 2)

		layout.addWidget(position_label, 11, 1)
		layout.addWidget(plot, 1, 1, 10, 1)
		
		self.resize(900, 550)
		self.show()

	def close_application(self):
		choice = QtGui.QMessageBox.question(self, 'Exit?', 
			"Are you sure that you want to exit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			print("Done!")
			sys.exit()
		else:
			pass

	def open_dialog(self):
		self.dialog.exec_()



def run():
	app = QtGui.QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())

run()
