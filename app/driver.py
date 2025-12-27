# Работа с веб-драйвером

from playwright.async_api import (
    async_playwright,Page,TimeoutError
)
from app.actions import (
    left_click,right_click,
    write,write_number
)

import asyncio

# Начало инициализации




class WebDriver:  
    TEST_SITE_TARGET = "https://google.com"

    EVENTS = {
        "left_click":left_click,
        "right_click":right_click,
        "write":write,
        "write_number":write_number
    }

    def __init__(self):
        self._browser = None
        self._context = None 


    def get_context(self):
        return self._context

    async def open_page(self,url):
        page = await self._context.new_page()
        await page.goto(url) 
        return page

    async def __call__(self,func):
        async with async_playwright() as p:
            self._browser = await p.chromium.launch(headless=True)
            self._context = await self._browser.new_context()

            print("Инициализация браузера и контекста завершена")
            await func(self)

    @classmethod 
    async def check(cls) -> bool:
        print("-Начало проверки WebDriver chromium-")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try: 
                response = await page.goto(cls.TEST_SITE_TARGET)
            except Exception as e:
                print("Похоже у тебя ошибка с сетью или же он слишком медленный")
                print(e)


            await browser.close()

        print("Веб-драйвер успешно работает")
        return True 

    
    @staticmethod
    async def execute(page : Page,event : str,query : str,data=None):
        locator = page.locator(query)

        try:
           await locator.wait_for()

        except TimeoutError:
            return f"{query} \n:Элемент не найден"     
        except Exception as e:
            print(e," ошибка в driver")

        event = WebDriver.EVENTS.get(event,None)
        if not event:
            return "Действие не найдено"

        await event(locator,data)