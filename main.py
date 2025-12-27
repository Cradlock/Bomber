from app.utils import (
    out_basic_tutorial
)
from app.manager import Manager

import asyncio

async def main():

    # проверка внешних зависимостей
    check_result = await Manager.check()
    if check_result is False:
        print("Ошибка при проверке зависимостей")
        return 


    # Это все в методе start()
      # получение всех ссылок сайтов + тегов с формами
      # открытие вкладок и отправка сообщений все многопоточно   

    await Manager.start()

if __name__ == "__main__":
    asyncio.run(main())
