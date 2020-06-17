import json
from datetime import datetime
import os


def TL():
    return datetime.today().strftime('%H:%M:%S.%f')


def Errcode(codename):
    d = {'None':1,'Authorization':2, 'PageAct':3,"NoNext":4,"NotSelect":5}
    return d.get(codename)

def GetLoginPass():
    with open("settings.json","r",encoding='utf-8') as setfile:
            data = json.load(setfile)
            return (data["login"],data["password"])

def GetGPXPath():
    with open("settings.json","r",encoding='utf-8') as setfile:
            data = json.load(setfile)
            return (data["gpxpath"])

class Log:
    def __init__(self, path=''):
        os.makedirs(path, exist_ok = True)
        self.fname: str = datetime.today().strftime(path + '%Y-%m-%dT%H%M%S') + '.log'

    def inp(self, str):
        try:
            self.f = open(self.fname, 'a', encoding='utf-8')
            self.f.write(str + '\n')
        except:
            pass
        finally:
            self.f.close()

    def inpt(self, str):
        try:
            self.f = open(self.fname, 'a', encoding='utf-8')
            self.f.write(TL() + '\t' + str + '\n')
        except:
            pass
        finally:
            self.f.close()
