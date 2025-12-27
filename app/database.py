import os 
import json 
import aiofiles

from app.utils import get_question

# Работа с json-бд

class Database:
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATABASE_PATH = f"{BASE_DIR}/hosts.json"
    
    required_fields = {
        "hosts":[]
    }

    hosts = None

    @classmethod
    async def setting(cls, file=None):
        async with aiofiles.open(cls.DATABASE_PATH, "w", encoding="utf-8") as file:
            await file.write(json.dumps(cls.required_fields, ensure_ascii=False, indent=4))

    @classmethod
    async def create(cls):
        if os.path.exists(cls.DATABASE_PATH) and os.path.isfile(cls.DATABASE_PATH):
            print(f"{cls.DATABASE_PATH}: файл уже существует")
            return

        async with aiofiles.open(cls.DATABASE_PATH, "w", encoding="utf-8") as file:
            await cls.setting(file)
            print(f"{cls.DATABASE_PATH}: файл создан")

    @classmethod
    async def check(cls) -> bool:
        if not os.path.exists(cls.DATABASE_PATH) or not os.path.isfile(cls.DATABASE_PATH):
            print("Базы данных не существует")
            print("Создание бд...")
            await cls.create()
            return False

        keys = []
        async with aiofiles.open(cls.DATABASE_PATH, "r", encoding="utf-8") as file:
            data = json.loads(await file.read())
            keys = data.keys()
        
        if not all(key in cls.required_fields.keys() for key in keys ):
            print("Бд не настроена")

            if get_question("Перенастроить бд?"):
                print("-Перенастройка-")
                await cls.setting()
    
            return 

        print("База данных успешно установлена")
        return True 

    @classmethod
    async def _load(cls):
        if cls.hosts is None:
          async with aiofiles.open(cls.DATABASE_PATH, "r", encoding="utf-8") as file:
            data = json.loads(await file.read())
            cls.hosts = data.get("hosts",[])
        
        return cls.hosts
            

    
    @classmethod
    async def get_data(cls,limit,offset = 0):
        data = await cls._load()

        pg_data = data[offset:offset + limit]

        if not pg_data:
            return None

        return pg_data
    
    @classmethod
    async def get_count(cls):
        data = await cls._load()
        if data is None: return 0
        return len(data)