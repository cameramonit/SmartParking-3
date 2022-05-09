import requests


class LicensePlate:
    PATH_TO_IMAGE = '/home'
    REG_NO = 'KA25Z8995'

    def __init__(self, PATH_TO_IMAGE):
        self.PATH_TO_IMAGE = PATH_TO_IMAGE

    def getLicensePlateNumber(self):
        file = {'file': open(self.PATH_TO_IMAGE, 'rb')}
        response=requests.post('https://smartparkingsystem1.herokuapp.com/',files=file)
        return response.json()
