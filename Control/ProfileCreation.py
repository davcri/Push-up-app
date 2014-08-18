'''
Created on Aug 18, 2014

@author: davide
'''
from View.Widgets.ProfileCreation import ProfileCreation as ProfileCreationWidget
from Foundation.Athlete import Athlete

class ProfileCreation():
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.dialog = ProfileCreationWidget()         
        
    def runCreationDialog(self):
        return self.dialog.getAthleteProfile()
        
    def runCreationDialogAndStore(self):
        athlete = self.dialog.getAthleteProfile()
        database = Athlete()
        
        database.store(athlete)
        
    
        