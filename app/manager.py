from app.database import Database
from app.driver import WebDriver
from app.tabs import Tab,Host
# класс для работы с сетью и отправкой сообщений и ассинхроностью
from app.settings import MAX_TABS,PHONE_NUMBER
from app.utils import (
    validate_phone_number,get_question
)
import time 

import asyncio

class Manager:
    
    sites_res = list()
    sites_with_error = list()
    time_start = None

    @classmethod
    async def start(cls):

        print(" ==== Начало работы ==== ") 
        cls.time_start = time.time()
        web_driver = WebDriver()
        
        await web_driver(cls.bomb)
        
        cls.result()
    
    @staticmethod
    def error(url):
        Manager.sites_with_error.append(url)

    @staticmethod
    def success(url):
        Manager.sites_res.append(url)


    @staticmethod
    async def bomb(web_driver):
        # Инициализация 
              
        tabs = [
            Tab(
                web_driver=web_driver,
                success_func=Manager.success,
                error_func=Manager.error) for _ in range(MAX_TABS)
        ]

        # Действие 

        ofs = 0        
        while True:
            hosts = await Database.get_data(limit=MAX_TABS,offset=ofs)
            
            if not hosts:
                print("Конец обработки")
                break
            
            hosts = [Host(**h) for h in hosts ]
            

            for idx,host in enumerate(hosts):
                tabs[idx].set_target_host(host)    
                print(host.url)   

            print("Отправка...")        
            
            await asyncio.gather(*(tab() for tab in tabs))

            ofs += MAX_TABS


    @classmethod
    def result(cls):
        time_n = time.time() - cls.time_start
        print(f"Заняло времени: {time_n}")
        print(f"Отправлено в: {len(cls.sites_res)}")

        print(f"Успешно в: {len(cls.sites_res) - len(cls.sites_with_error)}")
        
        if len(cls.sites_with_error) != 0: 
            if get_question("Показать сайты которые не работают"):
                for i in cls.sites_with_error:
                    print(i)
    
    @classmethod
    def close(cls):
        print(" -Закрытие ресурсов- ")



    @classmethod
    async def check(cls) -> bool:

        if not validate_phone_number(PHONE_NUMBER):
            print("Не верно задан номер")
            return 

        driver_check = await WebDriver.check()
        if not driver_check:
            print("Веб-драйвер не сработал")
            return False 

        db_check = await Database.check()
        if not db_check:
            print("База данных не сработала")
            return False

        return True



