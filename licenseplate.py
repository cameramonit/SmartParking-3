import requests


class LicensePlate:
    PATH_TO_IMAGE = '/home'
    REG_NO = 'KA25Z8995'

    def __init__(self, PATH_TO_IMAGE):
        self.PATH_TO_IMAGE = PATH_TO_IMAGE

    def getLicensePlateNumber(self):
        regions = ['in']  # Change to your country
        with open(self.PATH_TO_IMAGE, 'rb') as fp:
            response = requests.post(
                'https://api.platerecognizer.com/v1/plate-reader/',
                data=dict(regions=regions),  # Optional
                files=dict(upload=fp),
                headers={'Authorization': 'Token f52c6f2941e5bc78ad0ec88f04080a579f7b4509'})
        self.REG_NO = response.json()['results'][0]['plate']
        return response.json()['results'][0]['plate']
