'''
Created on Aug 16, 2014

@author: davide
'''

from PySide.QtGui import QDialog
from PySide.QtGui import QHBoxLayout, QVBoxLayout
from PySide.QtGui import QLabel, QPushButton, QListWidget 
from PySide.QtGui import QListWidgetItem, QIcon
from PySide.QtGui import QAbstractItemView
 
class ProfileSelection(QDialog):
    '''
    classdocs
    '''

    def __init__(self, athletesList):
        '''
        Constructor
        '''  
        QDialog.__init__(self)
        
        self.athletesList = athletesList
        self.selectedProfile = False
    
    def execDialogWindow(self):                
        hLayout = QHBoxLayout()
        vLayout = QVBoxLayout()
        
        # Label
        greeterText = QLabel("Welcome to <b>Pushup app</b>." + \
                             "<br><br> Select a profile:")
        vLayout.addWidget(greeterText)        
            
        # List 
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        # SingleSelection is the default value, but I prefer to be sure
        self.list.itemSelectionChanged.connect(self.activateOkButton) 
        
        for athlete in self.athletesList:
            iconW = QIcon.fromTheme("user-available")
            # doens't work on Mac and Windows
            # http://qt-project.org/doc/qt-4.8/qicon.html#fromTheme
            
            listW = QListWidgetItem(iconW, athlete._name)
            self.list.addItem(listW)
                
        vLayout.addWidget(self.list)
        
        vLayout.addLayout(hLayout)
        
        # Buttons
        self.okBtn = QPushButton("Ok")
        self.okBtn.setDisabled(True)
        self.okBtn.clicked.connect(self.okButtonSlot)
        self.list.itemDoubleClicked.connect(self.okButtonSlot)
        
        hLayout.addWidget(self.okBtn)
        
        cancelBtn = QPushButton("Cancel")      
        cancelBtn.clicked.connect(self.reject)
        
        removeProfileBtn = QPushButton("Remove Profile")
        removeProfileBtn.setDisabled(True)
        #removeProfileBtn.clicked.connect()
        
        hLayout.addWidget(cancelBtn)
        hLayout.addWidget(removeProfileBtn)        

        self.setLayout(vLayout)
        
        return self.exec_() 
    
    def okButtonSlot(self):
        self.selectedProfile = self.list.selectedItems()[0].text()
        self.accept()
    
    def getSelectedProfile(self):
        
        for athlete in self.athletesList:
            if self.selectedProfile == athlete._name:
                selectedAthlete = athlete
        
        return selectedAthlete
    
    def activateOkButton(self):
        self.okBtn.setDisabled(False)
        
    
        
