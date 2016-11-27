import sys
from PyQt4.QtGui import *
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

# add state_label

class Plot(pg.PlotWidget):

	def __init__(self):
		super(Plot, self).__init__()
		self.resize(660,600)
		self.setTitle('Acceleration-distance dependency graph')
		pg.setConfigOptions(antialias=True)
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

		self.stop_distance = 0
		self.t_limit = 0
		self.accel_distance = 0

		self.getPlotItem().setLabel('left', text = 'Distance (m)')
		self.getPlotItem().setLabel('bottom', text = 'Acceleration (m/s^2)')
		
	def set_distance(self, D):
		self.distance = int(D)

	def set_length(self, L):
		self.length = int(L)

	def set_t_yellow(self, time):
		self.t_yellow = int(time)

	def set_v_0(self, velocity):
		self.v_0 = int(velocity)*1000/float(3600)
	
	def set_v_limit(self, v_limit):
		self.v_limit = int(v_limit)*1000/float(3600)

	def set_a_max(self, acceleration):
		self.a_max = int(acceleration)

	def set_a_min(self, acceleration):
		if (int(acceleration) < 0):
			self.a_min = int(acceleration)
		else:
			self.a_min = -int(acceleration)

	def update_plot(self):
		if self.a_max != 0 and self.a_min!=0 and self.v_limit != 0 and self.t_yellow != 0:
			
			self.stop_distance = -self.v_0*self.v_0/float(2*self.a_min)
			self.t_limit = (self.v_limit - self.v_0)/float(self.a_max)

			if self.t_limit < self.t_yellow:
				self.accel_distance = self.v_0*self.t_limit + self.a_max*self.t_limit*self.t_limit/float(2) + self.v_limit*(self.t_yellow - self.t_limit)
			else:
				self.accel_distance = self.v_0*self.t_yellow + self.a_max*self.t_yellow*self.t_yellow/float(2)

		if self.a_min != 0:		
			X = np.empty([-self.a_min*100, ])
			Y = np.empty([-self.a_min*100, ])
			a = 0
			for i in range(100*self.a_min, 0):
				a = a - 1/100
				X[i] = a
				Y[i] = -self.v_0*self.v_0/float(2*a)
		else:
			pass

		#print a
		#print b
		p1 = self.plot(x = np.array([0, self.a_max]), y = np.array([0, self.accel_distance]), pen = 'b')
		try:
			p2 = self.getPlotItem().addItem(pg.PlotCurveItem(x = X, y = Y, pen = 'y'))
		except:
			pass
		
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

		l0 = self.getPlotItem().addLine(x = 0, movable = False, pen = {'color': "w"})
		l1 = self.getPlotItem().addLine(y = 0, movable = False, pen = {'color': "w"})
		self.enableAutoRange('y', 1)
		self.enableAutoRange('x', 1)


	def set_position_label(self, arg):
		self.label = arg

	def mouseMoved(self, evt):
  		mousePoint = self.getPlotItem().vb.mapSceneToView(evt[0])
  		self.label.setText("<span style='font-size: 15pt'> Coordinates: a = %0.2f (m/s^2), <span style='font-size: 15pt'> x = %0.2f (m)</span>" % (mousePoint.x(), mousePoint.y()))


	#def return_state(self):
	#	if self.accel_distance > self.distance+self.length:
	#		return "Accelerating"
	#	elif self.stop_distance < self.distance:
	#		return "Decelerating"
	#	else:
	#		return "!ALERT! A collision is unavoidable! Preaparing airbags!"


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

		self.whitedescription = QtGui.QLabel('x-axis and y-axis')
		self.reddescription = QtGui.QLabel('Distance from the intersection(line is movable)')
		self.greendescription = QtGui.QLabel('Distance from the intersection + Length of the intersection (line is movable)')
		self.violetdescription = QtGui.QLabel('Minimum acceleration of the car')
		self.lightbluedescription = QtGui.QLabel('Maximum acceleration of the car')
		self.yellowdescription = QtGui.QLabel('Graph in case of deceleration')
		self.bluedescription = QtGui.QLabel('Graph is case of acceleration')

		self.infolabel = QtGui.QLabel('\n\nYou can use mouse right button in order to make some corrections to the graph.\nAlso you can use mouse scroller (middle button) in order to zoom-in or -out')
		self.aboutlabel =QtGui.QLabel('\n\n\nTigran Sedrakyan\nAmerican University of Armenia\nSmart Car Graphing App, version 0.1 from 11/27/2016\nAll copyrights are reserved')
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
		self.plot = Plot()
		self.setWindowTitle('Smart Car App')
		self.setWindowIcon(QtGui.QIcon('car.png'))
		#self.state_label = QtGui.QLabel(self)
		#self.status = self.update_status()
		#print (self.status)
		self.dialog = Dialog()

		btn = QtGui.QPushButton("Exit", self)
		btn.clicked.connect(self.close_application)

		btn2 = QtGui.QPushButton("Coloring and info", self)
		btn2.clicked.connect(self.open_dialog)


		timeEdit = QtGui.QLineEdit(self)
		timeEdit.setPlaceholderText('Ty (s)');
		timeEdit.setValidator(QtGui.QIntValidator(2,4))
		timeEdit.textChanged.connect(lambda: self.plot.clear())
		timeEdit.textChanged.connect(lambda: self.plot.set_t_yellow(timeEdit.text()))
		timeEdit.textChanged.connect(self.plot.update_plot)
		timeEdit.textChanged.connect(self.plot.show)

		a_maxEdit = QtGui.QLineEdit(self)
		a_maxEdit.setPlaceholderText('Maximum Acceleration (m/s^2)');
		a_maxEdit.setValidator(QtGui.QIntValidator(0,3))
		a_maxEdit.textChanged.connect(lambda: self.plot.clear())
		a_maxEdit.textChanged.connect(lambda: self.plot.set_a_max(a_maxEdit.text()))
		a_maxEdit.textChanged.connect(self.plot.update_plot)
		a_maxEdit.textChanged.connect(self.plot.show)

		a_minEdit = QtGui.QLineEdit(self)
		a_minEdit.setPlaceholderText('Minimum Acceleration (m/s^2)');
		a_minEdit.setValidator(QtGui.QIntValidator(-3,0))
		a_minEdit.textChanged.connect(lambda: self.plot.clear())
		a_minEdit.textChanged.connect(lambda: self.plot.set_a_min(a_minEdit.text()))
		a_minEdit.textChanged.connect(self.plot.update_plot)
		a_minEdit.textChanged.connect(self.plot.show)

		v_0Edit = QtGui.QLineEdit(self)
		v_0Edit.setPlaceholderText('V0 (km/h)');
		v_0Edit.setValidator(QtGui.QIntValidator(20,80))
		v_0Edit.textChanged.connect(lambda: self.plot.clear())
		v_0Edit.textChanged.connect(lambda: self.plot.set_v_0(v_0Edit.text()))
		v_0Edit.textChanged.connect(self.plot.update_plot)
		v_0Edit.textChanged.connect(self.plot.show)

		v_limitEdit = QtGui.QLineEdit(self)
		v_limitEdit.setPlaceholderText('Speed Limit (km/h)');
		v_limitEdit.setValidator(QtGui.QIntValidator(40,90))
		v_limitEdit.textChanged.connect(lambda: self.plot.clear())
		v_limitEdit.textChanged.connect(lambda: self.plot.set_v_limit(v_limitEdit.text()))
		v_limitEdit.textChanged.connect(self.plot.update_plot)
		v_limitEdit.textChanged.connect(self.plot.show)

		distanceEdit = QtGui.QLineEdit(self)
		distanceEdit.setPlaceholderText('Distance from the intersection (m)');
		distanceEdit.setValidator(QtGui.QIntValidator(7,50))
		distanceEdit.textChanged.connect(lambda: self.plot.clear())
		distanceEdit.textChanged.connect(lambda: self.plot.set_distance(distanceEdit.text()))
		distanceEdit.textChanged.connect(self.plot.update_plot)
		distanceEdit.textChanged.connect(self.plot.show)

		lengthEdit = QtGui.QLineEdit(self)
		lengthEdit.setPlaceholderText('Length of the intersection (m)');
		lengthEdit.setValidator(QtGui.QIntValidator(7,20))
		lengthEdit.textChanged.connect(lambda: self.plot.clear())
		lengthEdit.textChanged.connect(lambda: self.plot.set_length(lengthEdit.text()))
		lengthEdit.textChanged.connect(self.plot.update_plot)
		lengthEdit.textChanged.connect(self.plot.show)

		position_label = QLabel()
		position_label.setText("<span style='font-size: 15pt, '>Coordinates: a=0 (m/s^2),   <span style='', 'font-size: 15pt'>x=0 (m)</span>")
		self.plot.set_position_label(position_label)

		layout = QtGui.QGridLayout(self)
		layout.addWidget(distanceEdit, 1, 2)
		layout.addWidget(lengthEdit, 2, 2)
		layout.addWidget(a_maxEdit, 3, 2)
		layout.addWidget(a_minEdit, 4, 2)
		layout.addWidget(timeEdit, 5, 2)
		layout.addWidget(v_0Edit, 6, 2)
		layout.addWidget(v_limitEdit, 7, 2)
		layout.addWidget(position_label, 11, 1)
		layout.addWidget(btn2, 10, 2)
		#layout.addWidget(self.state_label, 8, 2)
		layout.addWidget(self.plot, 1, 1, 10, 1)
		layout.addWidget(btn, 11, 2)
		
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

	#def update_status(self):
		#return self.plot.return_state()


def run():
	app = QtGui.QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())

run()
