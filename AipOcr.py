from aip import AipOcr
from configparser import ConfigParser


class Card(object):
    # def __init__(self):
    #     self.name = ''
    #     self.sex = ''
    #     self.nation = ''
    #     self.birthday = ''
    #     self.ID_numer = ''
    #     self.address = ''

    name = ''
    sex = ''
    nation = ''
    birthday = ''
    ID_numer = ''
    address = ''
    start = ''
    end = ''



class CardAip():

    def __init__(self, filePath):
        cp=ConfigParser()
        cp.read('config.ini')
        section = cp.sections()[0]
        APP_ID = cp.get(section,'APP_ID')
        API_KEY = cp.get(section,'API_KEY')
        SECRET_KEY = cp.get(section,'SECRET_KEY')

        print(APP_ID)
        print(API_KEY)
        print(SECRET_KEY)
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        self.filePath = filePath



    def getinfo(self,face):

        if face=='Front':
            with open(self.filePath, 'rb') as fp:
                image = fp.read()
            idCardSide = "front"
            result = self.client.idcard(image, idCardSide)
            print(result)
            card=Card()
            card.name = result["words_result"]["姓名"]["words"]
            card.sex = result["words_result"]["性别"]["words"]
            card.nation = result["words_result"]["民族"]["words"]
            card.birthday = result["words_result"]["出生"]["words"]
            card.ID_numer = result["words_result"]["公民身份号码"]["words"]
            card.address = result["words_result"]["住址"]["words"]


            # return (self.name,self.sex,self.nation,self.ID_numer,self.address,self.birthday)
            return card
        if face=='Back':
            with open(self.filePath, 'rb') as fp:
                image = fp.read()
            idCardSide = "back"
            result = self.client.idcard(image, idCardSide)
            print(result)
            card = Card()
            card.start = result["words_result"]["签发日期"]["words"]
            card.end = result["words_result"]["失效日期"]["words"]
            return card
if __name__ == '__main__':
    aip = CardAip('2.jpg')
    card =aip.getinfo()
    print(card.name)
