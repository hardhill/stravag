import time
from selenium import webdriver
from myfuncs import *
from servbot import *

def main():
    print('====================================================================')
    print('=                   STRAVA DOWNLOAD GPX files                      =')
    print('====================================================================')
    print(TL(),'Начало программы')
    GPXPath = GetGPXPath()
    login, password = GetLoginPass()
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : GPXPath}
    options.add_experimental_option("prefs",prefs)
    with webdriver.Chrome(options=options) as driver:
        wait:WebDriverWait = WebDriverWait(driver,10)
        bot = Bot(driver,wait)

        error = bot.Autorization(login,password)
        if error == 1:
            print(TL(), "Авторизация прошла успешно")
            error = bot.IsPageActivities()
        # if error == 1:
        #     print(TL(),"Загрузка страницы 'Тренировки'")
        #     error = bot.Select("Walk")
        if error == 1:
            print(TL(),"Загрузка страницы 'Тренировки'")
            trens = Trens()
            while True and error == 1:
                time.sleep(2)
                listActivity = bot.TrainingActivity()
                if len(listActivity)==0:
                    break
                else:
                    bot.SaveListActivities(trens,listActivity)
                buttonNext = bot.IsNextButton()
                if buttonNext:
                    buttonNext.click()
                else:
                    break

            trens.BackupList()
            print(TL(),"----------Сохранение GPX-------------")
            for oneTren in trens.All:
                url = oneTren['url']+"/export_gpx"
                driver.get(url)
                time.sleep(0.5)
        time.sleep(2)
        print(TL(),"Работа завершена")


if __name__ == '__main__':
    main()
