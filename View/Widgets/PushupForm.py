'''
Created on Aug 17, 2014

@author: davide
'''


from PySide.QtCore import Qt, QDate, Signal
from PySide.QtGui import QWidget, QDialog, \
                         QFormLayout, QVBoxLayout, QSpinBox, QCalendarWidget, \
                         QPushButton, QCheckBox
from Model.Pushup import Pushup as Pushup_Model
from Foundation.Pushup import Pushup as Pushup_Foundation
from datetime import date

class PushupForm(QDialog):
    '''
    classdocs
    '''
    pushupAdded = Signal()
    
    def __init__(self, athlete):
        '''
        Constructor
        '''
        QDialog.__init__(self)
        
        self.setWindowTitle("Pushup form")
        self.athlete = athlete
        self.pushupForm = QFormLayout()
        self.createGUI()
        
    def createGUI(self):
        self.series = QSpinBox()
        self.series.setMinimum(1)
        
        self.repetitions = QSpinBox()
        
        self.avgHeartRateToggle = QCheckBox()
        self.avgHeartRateToggle.toggled.connect(self._toggleHeartRateSpinBox)
        
        self.avgHeartRate = QSpinBox()
        self.avgHeartRate.setMinimum(40)
        self.avgHeartRate.setMaximum(250)
        self.avgHeartRate.setValue(120)
        self.avgHeartRate.setDisabled(True)
        
        self.date = QCalendarWidget()
        self.date.setMaximumDate(QDate.currentDate())
        
        self.addButton = QPushButton("Add pushup")
        self.addButton.setMaximumWidth(90)
        self.addButton.clicked.connect(self._createPushup)
        
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setMaximumWidth(90)
        self.cancelButton.clicked.connect(self.reject)
        
        self.pushupForm.addRow("Series", self.series)
        self.pushupForm.addRow("Repetitions", self.repetitions)
        self.pushupForm.addRow("Store average heart rate ? ", self.avgHeartRateToggle)
        self.pushupForm.addRow("Average Heart Rate", self.avgHeartRate)
        self.pushupForm.addRow("Exercise Date", self.date)
        
        btnsLayout = QVBoxLayout()
        btnsLayout.addWidget(self.addButton)
        btnsLayout.addWidget(self.cancelButton)        
        btnsLayout.setAlignment(Qt.AlignRight)
        
        layoutWrapper = QVBoxLayout()
        layoutWrapper.addLayout(self.pushupForm)
        layoutWrapper.addLayout(btnsLayout)
        
        self.setLayout(layoutWrapper)
        
        
    def _createPushup(self):
        print "Storing pushup"
        
        exerciseDate = self.date.selectedDate()
        exerciseDate = self.qDate_to_date(exerciseDate)
        
        if self.avgHeartRateToggle.isChecked():
            heartRate = self.avgHeartRate.value()
        else:
            heartRate = None
            
        pushup = Pushup_Model(self.athlete._name, 
                        exerciseDate, 
                        heartRate, 
                        self.series.value(),
                        self.repetitions.value())
        
        db = Pushup_Foundation()
        db.store(pushup)
        
        self.accept()
        self.pushupAdded.emit()       
        
        return pushup
    
    def _toggleHeartRateSpinBox(self):
        if self.avgHeartRateToggle.isChecked():
            self.avgHeartRate.setDisabled(False)
        else:
            self.avgHeartRate.setDisabled(True)
        
    def qDate_to_date(self, qDate):        
        return date(qDate.year(), qDate.month(),qDate.day())
        