import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = '7386356120:AAHGWZ9EqZsFh9XL_-q6daCK5r1a6mUzPuY'
HOROSCOPE_URL = 'https://orakul.com/horoscope/astrologic/general'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def get_zodiac_sign(day: int, month: int) -> str:
    zodiac_signs = [
        (120,'Козерог'), (218, 'Водолей'), (320, 'Рыбы'), (420, 'Овен'), 
        (521, 'Телец'), (621, 'Близнецы'), (722, 'Рак'), (823, 'Лев'), 
        (923, 'Дева'), (1023, 'Весы'), (1122, 'Скорпион'), (1222, 'Стрелец'), (1231, 'Козерог')
    ]

    date = int(f"{month:02d}{day:02d}")
    for end_date, sign in zodiac_signs:
        if date <= end_date:
            return sign

async def start(update: Update, context) -> None:
    await update.message.reply_text('Привет! Я бот гороскопов. Введите свою дату рождения в формате ДД.ММ.ГГГГ, чтобы получить гороскоп.')

async def get_horoscope(sign: str) -> str:
    zodiac_signs = [
        ('Козерог', '/capricorn'), ('Водолей','/aquarius'), ('Рыбы', '/pisces'), ('Овен', '/aries'), 
        ('Телец', '/taurus'), ('Близнецы', '/gemini'), ('Рак', '/cancer'), ('Лев', '/lion'), 
        ('Дева', '/virgo'), ('Весы', '/libra'), ('Скорпион', '/scorpio'), ('Стрелец', '/sagittarius')
    ]
    for sign_elem, url_sign in zodiac_signs:
        if sign == sign_elem:
            url = url_sign
    return HOROSCOPE_URL + url + '/today.html'

async def handle_date_of_birth(update: Update, context) -> None:
    try:
        dob = update.message.text
        day, month, year = map(int, dob.split('.'))
        sign = get_zodiac_sign(day, month)
        horoscope = await get_horoscope(sign)
        await update.message.reply_text(f'Ваш знак зодиака: {sign}\nВаш гороскоп на сегодня:\n{horoscope}')
    except ValueError:
        await update.message.reply_text('Неправильный формат даты. Пожалуйста, введите дату рождения в формате ДД.ММ.ГГГГ.')

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_date_of_birth))
    application.run_polling()

if __name__ == '__main__':
    main()
