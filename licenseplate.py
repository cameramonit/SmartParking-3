import requests
import os


class LicensePlate:
    FileName = 'image.jpg'
    REG_NO = 'KA25Z8995'

    def __init__(self,FileName):
        '''def __init__(self,PATH_TO_IMAGE):'''
        '''self.PATH_TO_IMAGE = PATH_TO_IMAGE'''
        self.FileName=os.getcwd()+'/'+FileName

    def getLicensePlateNumber(self):
        f=open(self.FileName, 'rb')
        file = {'file':f }
        #response=requests.post('https://smartparkingsystem1.herokuapp.com/',files=file)
        response=requests.post('https://parkingapi1.herokuapp.com/',files=file)
        f.close()
        if(response.ok==False):
            return None
        return response.json()
#Tests
#l=LicensePlate('download.jpg')
#print(l.getLicensePlateNumber())