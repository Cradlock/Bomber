from app.driver import WebDriver
import asyncio

# Работа с конкретным действием
class Action:
    def __init__(self,event,query,data=None,**kwargs):
        self.event = event 
        self.query = query
        self.data = data

    

    async def __call__(self,page):
        # здесь будет само действие (взять элемент и выполнить)
        result = await WebDriver.execute(page,self.event,self.query,self.data)
        return result 

    def __str__(self):
        return f"{self.event} -> {self.type_query}({self.query}) данные: {self.data}"


# Работа с конкретным сайтом
class Host:
    def __init__(self,url,actions):
        self.url = url 
        self.actions = []

        for i in actions:
            self.actions.append( Action(**i) )
    
    async def activate_action(self,page):
        actions = [ act(page) for act in self.actions  ]
        return await asyncio.gather(*actions)


# Работа со всей вкладкой
class Tab:
    def __init__(self,web_driver,success_func,error_func):
        self.success_func = success_func 
        self.error_func = error_func 

        self.web_driver : WebDriver = web_driver
        self.target_host : Host = None 

    def set_target_host(self,host : Host):
        self.target_host = host

    async def __call__(self):
        # инициализация
        url = self.target_host.url
        self.success_func(url)
        try:
            page = await self.web_driver.open_page(url)
        except Exception as e:
            self.error_func(f"{url} \nerror: {e}")
            return


        # Активация действий
        errors = await self.target_host.activate_action(page)
        for res in errors:
            if res:
                print(f"{url} \nошибка: {res} ")

        # Закрытие
        await page.close()
        
    
    def __str__(self):
        return f"{url} <- {self.actions}"
    