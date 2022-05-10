from reprlib import aRepr
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import os


class Cloud:
    slot_list = []
    AREA_ID='1'
    PATH_TO_CREDENTIALS = '/smartparkingsystem-5ffb7-2f4717e68ead.json'
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
            'TIME_IN': firestore.firestore.SERVER_TIMESTAMP,
            'TIME_OUT': -1
            #,'LOCATION': firestore.firestore.GeoPoint(74, 15),
        })


    def getFreeSlot(self):
        for slot in self.slot_list:
            slot_info = self.firestore_db.collection(self.AREA_ID).document(str(slot)).get().to_dict()
            if not slot_info['ASSIGNED']:
                return slot
        return -1


    def setSlot(self, FREE_SLOT, REG_NO):
        slot = self.firestore_db.collection(self.AREA_ID).document(str(FREE_SLOT))
        slot.set({
            'ASSIGNED': True,
            'EMPTY': True,
            'REG_NO': REG_NO,
            'TIME_IN': firestore.firestore.SERVER_TIMESTAMP,
            'TIME_OUT': -1
            #,'LOCATION': self.LOCATION_COORDINATES,
        })


    def setSlotStatus(self, SLOT_NO, SLOT_STATUS):
        slot = self.firestore_db.collection(self.AREA_ID).document(str(SLOT_NO))
        slot.set({
            'ASSIGNED': True,
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
                'TIME_IN': firestore.firestore.SERVER_TIMESTAMP,
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


#c=Cloud('smartparkingsystem-5ffb7-2f4717e68ead.json',[12,10])
#c.createArea(4,1,[10,5])
    