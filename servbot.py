import json
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from myfuncs import Errcode, TL


class Bot:
    def __init__(self,driver,wait):
        self.driver:WebDriver = driver
        self.wait:WebDriverWait = wait
        element = None
    def Autorization(self,login,password):
        self.driver.get('https://strava.com/athlete/training')
        try:
            element = self.wait.until(EC.presence_of_element_located((By.ID,"email")))
        except:
            return Errcode("Authorization")
        if element:
            self.driver.execute_script("document.getElementById('email').setAttribute('value','{login}')".format(login=login))
            self.driver.execute_script("document.getElementById('password').setAttribute('value','{password}')".format(password=password))
            try:
                button = self.driver.find_element_by_id("login-button")
                button.click()
            except:
                return Errcode("Authorization")
        return Errcode("None")

    def IsPageActivities(self):
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"activity-count")))
            if len(elements)>0:
                return Errcode('None')
        except Exception as err:
            print("(E) страница не загружена",err)
            return Errcode("PageAct")

    def TrainingActivity(self):
        try:
            pagination = self.wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='simple pagination']")))
            table = self.wait.until(EC.presence_of_element_located((By.XPATH, "//script[@id='activity-template']")))
            # self.wait.until_not(EC.presence_of_element_located((By.XPATH,"//span[@class='status']")))
            list = self.driver.find_elements_by_class_name("training-activity-row")
            return list
        except Exception as err:
            print("(E) список не получен",err)
            return []

    def IsNextButton(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='simple pagination']")))
            next_button = self.wait.until(EC.presence_of_element_located((By.XPATH,"//button[@class='btn btn-default btn-sm next_page']")))
            return next_button
        except Exception as err:
            print("(E) кнопка не активна",err)
            return None

    def SaveListActivities(self, trens, listActivity):
        for item in listActivity:
            try:
                row:WebElement = item
                cells = row.find_elements_by_tag_name("td")
                sport = cells[0].text
                datet = cells[1].text
                title = cells[2].text
                url = cells[2].find_element_by_tag_name("a").get_attribute("href")
                dura = cells[3].text
                length = cells[4].text
                trens.Add(sport=sport,datet=datet,title=title,dura=dura,length=length,url=url)
            except:
                pass

    def Select(self, param):
        try:
            sel = self.driver.find_element_by_xpath("//select[@id='activity_type']")
            for option in sel.find_elements_by_tag_name('option'):
                if option.get_attribute("value") == param:
                    option.click()
                    return Errcode("None")
        except Exception as err:
            print("(E) ошибка выбора типа спорта",err)
            return Errcode("NotSelect")





class Trens:
    def __init__(self):
        self.All = []
    def Add(self,sport,datet,title,dura,length,url):
        tren = {"sport":sport,"date":datet,"title":title,"dura":dura,"length":length,"url":url}
        self.All.append(tren)

    def BackupList(self):
        print(TL(),"Записываю {n} тренировок".format(n=len(self.All)))
        js = json.dumps(self.All,indent=4,ensure_ascii=False).encode("utf8")
        print(js.decode("utf8"))
        with open('gpxdata.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.All, json_file,ensure_ascii=False)

    def AllActivities(self):
        return self.All


