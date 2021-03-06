'''
Created on Sep 30, 2014

@author: davide
'''
from datetime import date

from PySide.QtCore import QDate
from PySide.QtGui import QDoubleSpinBox
from PySide.QtGui import QWidget
from PySide.QtGui import QFormLayout, QVBoxLayout, QHBoxLayout
from PySide.QtGui import QLineEdit, QCalendarWidget, QRadioButton

from Model.Athlete import Athlete

class ProfileFormWidget(QWidget):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        QWidget.__init__(self)
        self._initGUI()
        
    def _initGUI(self):
        self.layout = QVBoxLayout()
        self.form = QFormLayout()
        
        self.name = QLineEdit()
        self.surname = QLineEdit()
        
        self.birthdate = QCalendarWidget()
        self.birthdate.setGridVisible(True)
        self.birthdate.setMinimumDate(QDate(1850,1,1))
        self.birthdate.setMaximumDate(QDate.currentDate())
        
        self.male = QRadioButton("Male")
        self.male.setChecked(True)
        self.female = QRadioButton("Female")
        
        self.height = QDoubleSpinBox()
        self.height.setMaximum(250)
        self.height.setMinimum(50)
        self.height.setValue(165)
        self.height.setSuffix(" cm")
        
        self.mass = QDoubleSpinBox()
        self.mass.setMaximum(300)
        self.mass.setMinimum(20)
        self.mass.setValue(60)
        self.mass.setSuffix(" Kg")
        
        btnLayout = QVBoxLayout()
        
        self.form.addRow("Name", self.name)
        self.form.addRow("Surname", self.surname)
        self.form.addRow("Birth date",self.birthdate)
        
        sexLayout = QHBoxLayout()
        sexLayout.addWidget(self.male)
        sexLayout.addWidget(self.female)
        self.form.addRow("Sex", sexLayout)
        
        self.form.addRow("Height", self.height)
        self.form.addRow("Mass", self.mass)
                
        self.layout.addLayout(self.form)
        self.layout.addLayout(btnLayout)
        self.setLayout(self.layout)
        
    def getLayout(self):
        return self.layout
    
    def getWidget(self):
        widget = QWidget()
        widget.setLayout(self.layout)
    
        return widget
    
    def setProfile(self, athlete):
        self.name.setText(athlete._name)
        self.surname.setText(athlete._surname)
        self.birthdate.setSelectedDate(athlete._birthDate)
        
        if athlete._sex=="Male":
            self.male.setChecked(True)
        else:
            self.female.setChecked(True)
            
        self.height.setValue(athlete._height)
        self.mass.setValue(athlete._mass)
                
    def getProfile(self):        
        qDate = self.birthdate.selectedDate()
        birthDate = self.qDate_to_date(qDate)
        
        athleteProfile = Athlete(self.name.text(),
                                 self.surname.text(),
                                 self._getSex(),
                                 birthDate,
                                 self.height.value(),
                                 self.mass.value())
        return athleteProfile 
    
    def qDate_to_date(self, qDate):        
        return date(qDate.year(), qDate.month(),qDate.day())
     
    def _getSex(self):
        if (self.male.isChecked()):
            return "Male"
        elif (self.female.isChecked()):
            return "Female"
        else :
            print "Error: No sex selected"
            return False
    