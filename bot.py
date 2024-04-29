import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import F
from aiogram.utils.formatting import (
    HashTag
)

from config_reader import config
from datetime import datetime
from coinmarketcapapi import CoinMarketCapAPI
import locale
import pytz



# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
session = AiohttpSession(proxy="socks5://127.0.0.1:2080/")
bot = Bot(token=config.bot_token.get_secret_value(), session=session)
cmc = CoinMarketCapAPI(api_key=config.CoinMarketCapAPI.get_secret_value())

desired_timezone = pytz.timezone('Asia/Shanghai')
# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
        types.KeyboardButton(text="💵 USD/CNY 💰"),
        types.KeyboardButton(text="💵 USD/RUB 💰"),],
        [
        types.KeyboardButton(text="💵 TON/USD 💰"),
        types.KeyboardButton(text="💵 BTC/USD 💰")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Какая валюта Вас интересует??", reply_markup=keyboard)



@dp.message(F.text.lower() == "💵 usd/cny 💰")
async def with_puree(message: types.Message):
    rep = cmc.cryptocurrency_quotes_latest(symbol='USDT', convert = "CNY")
    
    
    price = round(rep.data['USDT'][0]['quote']['CNY']['price'], 2 )

    date = datetime.fromisoformat(rep.timesamp).astimezone(desired_timezone).strftime("%d.%m.%Y")
    time = datetime.fromisoformat(rep.timesamp ).astimezone(desired_timezone).strftime("%H:%M")
    
    percent_change_24h = round(rep.data['USDT'][0]['quote']['CNY']['percent_change_24h'], 2 )
    percent_change_7d = round(rep.data['USDT'][0]['quote']['CNY']['percent_change_7d'], 2 )    
    
    if percent_change_24h < 0:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▼ {percent_change_24h_price} CNY ({percent_change_24h}%)"
        percent_change_24h_text = f"📉 Изменение за сутки:\n{percent_change_24h}"
    else:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▲ {percent_change_24h_price} CNY ({percent_change_24h}%)"
        percent_change_24h_text = f"📈 Изменение за сутки:\n{percent_change_24h}"
    

    if percent_change_7d < 0:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▼ {percent_change_7d_price} CNY ({percent_change_7d}%)"
        percent_change_7d_text = f"📉 Изменение за неделю:\n{percent_change_7d}"
    else:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▲ {percent_change_7d_price} CNY ({percent_change_7d}%)"
        percent_change_7d_text = f"📈 Изменение за неделю:\n{percent_change_7d}"
    
    text = f'''📈💵 Курс USD к CNY 💰📉\n\n📆 Дата: {date}\n🕒 Время: {time}\n\n💱 1 USD = {price} CNY\n\n{percent_change_24h_text}\n\n{percent_change_7d_text}'''
    await message.reply(text)


@dp.message(F.text.lower() == "💵 usd/rub 💰")
async def with_puree(message: types.Message):
    rep = cmc.cryptocurrency_quotes_latest(symbol='USDT', convert = "RUB")
    
    
    price = round(rep.data['USDT'][0]['quote']['RUB']['price'], 2 )

    date = datetime.fromisoformat(rep.timesamp).astimezone(desired_timezone).strftime("%d.%m.%Y")
    time = datetime.fromisoformat(rep.timesamp ).astimezone(desired_timezone).strftime("%H:%M")
    
    percent_change_24h = round(rep.data['USDT'][0]['quote']['RUB']['percent_change_24h'], 2 )
    percent_change_7d = round(rep.data['USDT'][0]['quote']['RUB']['percent_change_7d'], 2 )    
    
    if percent_change_24h < 0:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▼ {percent_change_24h_price} RUB ({percent_change_24h}%)"
        percent_change_24h_text = f"📉 Изменение за сутки:\n{percent_change_24h}"
    else:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▲ {percent_change_24h_price} RUB ({percent_change_24h}%)"
        percent_change_24h_text = f"📈 Изменение за сутки:\n{percent_change_24h}"
    

    if percent_change_7d < 0:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▼ {percent_change_7d_price} RUB ({percent_change_7d}%)"
        percent_change_7d_text = f"📉 Изменение за неделю:\n{percent_change_7d}"
    else:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▲ {percent_change_7d_price} RUB ({percent_change_7d}%)"
        percent_change_7d_text = f"📈 Изменение за неделю:\n{percent_change_7d}"
    
    text = f'''📈💵 Курс USD к RUB 💰📉\n\n📆 Дата: {date}\n🕒 Время: {time}\n\n💱 1 USD = {price} RUB\n\n{percent_change_24h_text}\n\n{percent_change_7d_text}'''
    await message.reply(text)


@dp.message(F.text.lower() == "💵 ton/usd 💰")
async def with_puree(message: types.Message):
    rep = cmc.cryptocurrency_quotes_latest(slug='toncoin', convert = "USD")
    
    
    price = round(rep.data['11419']['quote']['USD']['price'], 2 )

    date = datetime.fromisoformat(rep.timesamp).astimezone(desired_timezone).strftime("%d.%m.%Y")
    time = datetime.fromisoformat(rep.timesamp ).astimezone(desired_timezone).strftime("%H:%M")
    
    percent_change_24h = round(rep.data['11419']['quote']['USD']['percent_change_24h'], 2 )
    percent_change_7d = round(rep.data['11419']['quote']['USD']['percent_change_7d'], 2 )    
    
    if percent_change_24h < 0:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▼ {percent_change_24h_price} USD ({percent_change_24h}%)"
        percent_change_24h_text = f"📉 Изменение за сутки:\n{percent_change_24h}"
    else:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▲ {percent_change_24h_price} USD ({percent_change_24h}%)"
        percent_change_24h_text = f"📈 Изменение за сутки:\n{percent_change_24h}"
    

    if percent_change_7d < 0:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▼ {percent_change_7d_price} USD ({percent_change_7d}%)"
        percent_change_7d_text = f"📉 Изменение за неделю:\n{percent_change_7d}"
    else:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▲ {percent_change_7d_price} USD ({percent_change_7d}%)"
        percent_change_7d_text = f"📈 Изменение за неделю:\n{percent_change_7d}"
    
    text = f'''📈💵 Курс TON к USD 💰📉\n\n📆 Дата: {date}\n🕒 Время: {time}\n\n💱 1 TON = {price} USD\n\n{percent_change_24h_text}\n\n{percent_change_7d_text}'''
    await message.reply(text)


@dp.message(F.text.lower() == "💵 btc/usd 💰")
async def with_puree(message: types.Message):
    rep = cmc.cryptocurrency_quotes_latest(slug='bitcoin', convert = "USD")
    price = round(rep.data['1']['quote']['USD']['price'], 2 )

    date = datetime.fromisoformat(rep.timesamp).astimezone(desired_timezone).strftime("%d.%m.%Y")
    time = datetime.fromisoformat(rep.timesamp ).astimezone(desired_timezone).strftime("%H:%M")
    
    percent_change_24h = round(rep.data['1']['quote']['USD']['percent_change_24h'], 2 )
    percent_change_7d = round(rep.data['1']['quote']['USD']['percent_change_7d'], 2 )
    if percent_change_24h < 0:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▼ {percent_change_24h_price} USD ({percent_change_24h}%)"
        percent_change_24h_text = f"📉 Изменение за сутки:\n{percent_change_24h}"
    else:
        percent_change_24h_price = round((price*percent_change_24h)/100, 2)
        percent_change_24h = f"▲ {percent_change_24h_price} USD ({percent_change_24h}%)"
        percent_change_24h_text = f"📈 Изменение за сутки:\n{percent_change_24h}"
    

    if percent_change_7d < 0:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▼ {percent_change_7d_price} USD ({percent_change_7d}%)"
        percent_change_7d_text = f"📉 Изменение за неделю:\n{percent_change_7d}"
    else:
        percent_change_7d_price = round((price*percent_change_7d)/100, 2)
        percent_change_7d = f"▲ {percent_change_7d_price} USD ({percent_change_7d}%)"
        percent_change_7d_text = f"📈 Изменение за неделю:\n{percent_change_7d}"
    
    text = f'''📈💵 Курс BTC к USD 💰📉\n\n📆 Дата: {date}\n🕒 Время: {time}\n\n💱 1 BTC = {price} USD\n\n{percent_change_24h_text}\n\n{percent_change_7d_text}'''
    await message.reply(text)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())