from aiogram import Bot,executor,Dispatcher,types
from aiogram.dispatcher import FSMContext
import requests
from bs4 import BeautifulSoup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '5557676933:AAFl9LpMWkhkrj1RQuRJ8bM21Cxq8zhqCcM'
bot = Bot(TOKEN)
class Botik(StatesGroup):
    pars = State()
    pars2 = State()
dp = Dispatcher(bot,storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def main(message: types.Message):
    await message.answer('Введите город(на латинице)')
    await Botik.pars.set()

@dp.message_handler(state=Botik.pars)
async def on(message: types.Message, state: FSMContext):
    s_city = message.text
    res = requests.get("http://api.openweathermap.org/data/2.5/find",params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': '721920790bf594f476565d8bf426f577'})
    data = res.json()
    city_id = data['list'][0]['id']
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': '721920790bf594f476565d8bf426f577'})
    data = res.json()
    cond = data['weather'][0]['description']
    temp = data['main']['temp']
    temp_min = data['main']['temp_min']
    temp_max = data['main']['temp_max']
    await message.answer(f'Погода: {cond}\nТемпература: {temp}\nТемпература минимальная: {temp_min}\nТерпература максимальная: {temp_max}')
    await state.finish()
if __name__ == '__main__':
    executor.start_polling(skip_updates=True,dispatcher=dp)