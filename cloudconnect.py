import time
import datetime
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import pytz
import os
from parkingprice import calculate_parking_price

IST = pytz.timezone('Asia/Kolkata')

class Cloud:
    slot_list = []
    AREA_ID='1'
    PATH_TO_CREDENTIALS = 'smartparkingsystem-5ffb7-2f4717e68ead.json'
    FIRST_SLOT_NO = 1
    LAST_SLOT_NO = 4
    firestore_db = 1
    LOCATION_COORDINATES = firestore.firestore.GeoPoint(12, 12)


    def __init__(self, CREDENTIALS_FILE_NAME,AREA_ID=None,AREA_COORDINATES=None):
        self.PATH_TO_CREDENTIALS = os.getcwd() +'/'+ CREDENTIALS_FILE_NAME

        if(AREA_COORDINATES!=None):
            self.AREA_COORDINATES = firestore.firestore.GeoPoint(AREA_COORDINATES[0],AREA_COORDINATES[1])

        cred = credentials.Certificate(self.PATH_TO_CREDENTIALS)
        firebase_admin.initialize_app(cred)
        self.firestore_db = firestore.client()

        if AREA_ID!=None:
            self.AREA_ID=AREA_ID

        slot_list=self.firestore_db.collection(self.AREA_ID).get()

        n=len(slot_list)

        for i in range(n-1):
            self.slot_list.append(i)
 

    def setGeneralLocation(self):
        area=self.firestore_db.collection(self.AREA_ID).document('GeneralLocation')
        area.set({
            'AreaLocation':self.AREA_COORDINATES
        })
    
    def setAreaId(self,AREA_ID,AREA_COORDINATES):
        self.AREA_ID=AREA_ID
        self.AREA_COORDINATES=AREA_COORDINATES


    def clearSlot(self, SLOT_NO):
        slot = self.firestore_db.collection(self.AREA_ID).document(str(SLOT_NO))
        slot.set({
            'ASSIGNED': False,
            'EMPTY': True,
            'REG_NO': '',
            'TIME_IN': -1,
            'TIME_OUT': -1
            #,'LOCATION': firestore.firestore.GeoPoint(74, 15),
        })


    def getFreeSlot(self):
        for slot in self.slot_list:
            slot_info = self.firestore_db.collection(self.AREA_ID).document(str(slot)).get().to_dict()
            if not slot_info['ASSIGNED']:
                return slot
        return -1

    
    def assignSlot(self, FREE_SLOT, REG_NO):
        slot = self.firestore_db.collection(self.AREA_ID).document(str(FREE_SLOT))
        slot.set({
            'ASSIGNED': True,
            'EMPTY': True,
            'REG_NO': REG_NO,
            'TIME_IN': datetime.datetime.now(IST),
            'TIME_OUT': -1
            #,'LOCATION': self.LOCATION_COORDINATES,
        })
    
    def searchRegistrationNumber(self,REG_NO):
        slots=self.firestore_db.collection(self.AREA_ID)
        slots=slots.where('REG_NO','==',REG_NO)
        slot=slots.get()
        if(len(slot)==0):
            return None
        slot_data=(slot[0].to_dict())
        return [slot[0].id,slot_data['TIME_IN']]
        

    def getSlotStatus(self,SLOT_NO):
        return self.firestore_db.collection(self.AREA_ID).document(str(SLOT_NO)).get().to_dict()


    def setSlotStatus(self, SLOT_NO, SLOT_STATUS):
        slot = self.firestore_db.collection(self.AREA_ID).document(str(SLOT_NO))
        slot.update({
            'EMPTY': SLOT_STATUS
        })
    
    
    def createArea(self,AREA_ID,SLOT_NO,AREA_COORDINATES):
        self.deleteArea(str(AREA_ID))
        for i in range(1,SLOT_NO+1):
            slot = self.firestore_db.collection(str(AREA_ID)).document(str(i))
            slot.set({
                'ASSIGNED': False,
                'EMPTY': True,
                'REG_NO': '',
                'TIME_IN': -1,
                'TIME_OUT': -1
                #,'LOCATION': firestore.firestore.GeoPoint(74, 15),
            })
        
        location_param=self.firestore_db.collection(str(AREA_ID)).document('GeneralLocation')
        location_param.set({
            'AreaLocation':firestore.firestore.GeoPoint(AREA_COORDINATES[0],AREA_COORDINATES[1])
        })

    def deleteArea(self,AREA_ID):
        area=self.firestore_db.collection(str(AREA_ID)).stream()
        areaData=self.firestore_db.collection(str(AREA_ID)).get()
        if len(areaData):
            for i in area:
                i.reference.delete()

# c=Cloud('smartparkingsystem-5ffb7-2f4717e68ead.json',AREA_ID='1',AREA_COORDINATES=[10,12])
# # #c.assignSlot(1,'KA')
# entry=(c.searchRegistrationNumber('KA')[1])
# exit=datetime.datetime.now(IST)
# print(str(exit-entry).split(' days, '))
