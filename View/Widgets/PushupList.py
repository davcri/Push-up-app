'''
Created on Aug 17, 2014

@author: davide
'''

from PySide.QtCore import Qt, Signal
from PySide.QtGui import QWidget, QListWidget, QVBoxLayout, QListWidgetItem,\
                         QTreeWidget, QTreeWidgetItem, QAction, QMenu, QCursor
                         

class PushupList(QWidget):
    '''
    classdocs
    ''' 
    
    deletePushup = Signal(int)
    deleteDay = Signal()
    
    def __init__(self, pushups):
        '''
        Constructor
        '''
        QWidget.__init__(self)
        
        self.pushups = pushups
        self.createGUI()
    
    def createGUI(self):
        self.layout = QVBoxLayout()
        # self.pushupsListWidget = QListWidget(self)
        self.pushupsListWidget = QTreeWidget(self)
        
        self.pushupsListWidget.setMinimumHeight(250)        
        self.pushupsListWidget.setMaximumWidth(500)
        self.pushupsListWidget.setAlternatingRowColors(True)
        
        self.pushupsListWidget.doubleClicked.connect(self.doubleClick_Test)
        # WARNING : double click on top level Item is  not handled, so it will 
        # produce a AttributeError: 'NoneType' object has no attribute '_id'
        
        self.pushupsListWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pushupsListWidget.customContextMenuRequested.connect(self._customMenu)
        
        self._populateTree()
        
        self.layout.addWidget(self.pushupsListWidget)
        
        self.setLayout(self.layout)   
    
    # Slot
    def _customMenu(self):
        selectedItems = self.pushupsListWidget.selectedItems()
        
        if selectedItems is not None :
            selectedItem = selectedItems[0] 
            
            if selectedItem.parent() is not None : # Child Item selected
                menu = QMenu()
                
                self.pushupId = selectedItem.data(0, Qt.UserRole)._id
                
                delete = QAction(self.pushupsListWidget)
                delete.setText("Delete this pushup")
                delete.triggered.connect(self._emitDeleteSignal)
                menu.addAction(delete)
                menu.exec_(QCursor.pos())
            else : # Top level Item selected
                menu = QMenu()
             
                delete = QAction(self.pushupsListWidget)
                delete.setText("Delete this day and all of its exercises")
                delete.triggered.connect(self._populateTree)
                menu.addAction(delete)
                menu.exec_(QCursor.pos())
    
    def _emitDeleteSignal(self):
        self.deletePushup.emit(self.pushupId)

    def _populateTree(self):
        self.pushupsListWidget.clear()
        self.pushupsListWidget.setColumnCount(4)
        self.pushupsListWidget.setHeaderLabels(["Date", "Series", "Repetitions",
                                                "Average Heart Rate"])
        self.pushupsListWidget.setSortingEnabled(True)
        
        pushupDict = self._getPushupDictionary()

        for dayOfExercise in pushupDict:                  
             
            dateItem = QTreeWidgetItem()
            dateItem.setText(0, "\n"+dayOfExercise+"\n")
            
            self.pushupsListWidget.addTopLevelItem(dateItem)
             
            for pushup in pushupDict[dayOfExercise]:
                pushupItem = QTreeWidgetItem()
                
                pushupItem.setText(1, str(pushup._series))
                pushupItem.setText(2, str(pushup._repetitions))
                pushupItem.setText(3, str(pushup._averageHeartRate))
                pushupItem.setData(0, Qt.UserRole, pushup)
                
                dateItem.addChild(pushupItem)       
         
    def doubleClick_Test(self):
        selectedPushups = self.pushupsListWidget.selectedItems()[0].data(0, Qt.UserRole)
        print selectedPushups._id            
        
    def reloadPushupsList(self, pushups):
        self.pushups = pushups
        self._populateTree()
        
    def _populateListWidget(self):
        ''' 
        unused old method
        '''
        
        self.pushupsListWidget.clear()
        
        pushupDict = self._getPushupDictionary()
        
        for dayOfExercise in pushupDict:                  
            listItemString = "Date : "+ dayOfExercise + "\n"
            listItem_Data =[]
            
            for pushup in pushupDict[dayOfExercise]:
                listItemString += "Series : " + str(pushup._series) + \
                                  " Repetition : " + str(pushup._repetitions) + "\n"
                listItem_Data.append(pushup)
                             
            listItem = QListWidgetItem(listItemString)
            listItem.setData(Qt.UserRole, listItem_Data)
            
            self.pushupsListWidget.addItem(listItem)        
            
    def _getPushupDictionary(self):
        '''
        Returns a dictionary with the following structure : 
        - Key : date of the exercises. Type datetime.date
        - Value : list containing pushups made that day . Type : [Pushup model object]    
        
        example : 
        {
            2014-08-18: [pushupModelObj1, pushupModelObj2, pushupModelObj3],
            2014-08-19: [pushupModelObj4, pushupModelObj5, pushupModelObj6]
        } 
        '''
        pushupDateList = {} # dictionary initialization
        
        for pushup in self.pushups:
            if not pushupDateList.has_key(pushup._date):
                pushupsList = [pushup]
                pushupDateList[pushup._date] = pushupsList
            else:
                pushupDateList[pushup._date].append(pushup)
                 
#         for k in pushupDateList.keys():
#             print k
#             
#             for pu in pushupDateList[k]:
#                 print pu
         
        return pushupDateList    
        
        
        
        
        
        
        
        
        
        
        
        
        
        