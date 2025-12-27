from app.settings import PHONE_NUMBER

from playwright.async_api import Locator

async def left_click(locator : Locator,data=None):
    await locator.click()

async def right_click(locator : Locator,data=None):
    await locator.click(button="right") 


async def write(locator : Locator,data=None):
    await locator.fill(data)

async def write_number(locator : Locator,data=None):
    await loctor.fill(PHONE_NUMBER)



