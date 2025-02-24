import requests
import telebot

BOT_TOKEN = 'توکن'  # توکن ربات خود را در اینجا قرار دهید
bot = telebot.TeleBot(BOT_TOKEN)

robot_active = True

def get_available_cryptos():
    url = "https://api.nobitex.ir/market/stats"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {symbol.split('-')[0]: symbol.split('-')[0] for symbol in data["stats"].keys()}
    return {}
crypto_map = {
    "تتر": "usdt", "بیت‌کوین": "btc", "اتریوم": "eth", "ریپل": "xrp", "کاردانو": "ada",
    "دوج‌کوین": "doge", "پولکادات": "dot", "لایت‌کوین": "ltc", "ترون": "trx",
    "بیت‌کوین‌کش": "bch", "بایننس‌کوین": "bnb", "ماتیک": "matic", "یونی‌سواپ": "uni",
    "شیبا": "shib", "اتم": "atom", "اتریوم‌کلاسیک": "etc", "استلار": "xlm",
    "ایاس": "eos", "آوالانچ": "avax", "چین‌لینک": "link", "فانتوم": "ftm",
    "نیر": "near", "شیلیز": "chz", "فایل‌کوین": "fil", "تتا": "theta",
    "هدرا": "hnt", "آوی": "aave", "پنکیک‌سواپ": "cake", "مونرو": "xmr",
    "زی‌کش": "zec", "دش": "dash", "نئو": "neo", "تون‌کوین": "ton",
    "نات‌کوین": "nwc"
}

crypto_list = get_available_cryptos()
crypto_list.update(crypto_map)

def get_crypto_price(symbol):
    url = "https://api.nobitex.ir/market/stats"
    payload = {"srcCurrency": symbol, "dstCurrency": "rls"}
    response = requests.get(url, params=payload)

    if response.status_code == 200:
        data = response.json()
        stats = data["stats"].get(f"{symbol}-rls")
        if stats:
            latest = int(stats["latest"])  # قیمت لحظه‌ای به تومان
            best_sell = int(stats["bestSell"])  # بالاترین قیمت
            best_buy = int(stats["bestBuy"])  # کمترین قیمت
            trend = "📈 افزایشی ⬆" if latest > best_buy else "📉 کاهشی ⬇"

            return latest, best_sell, best_buy, trend
    return None, None, None, None
def get_usdt_price():
    latest, _, _, _ = get_crypto_price("usdt")
    return latest if latest else None
@bot.message_handler(func=lambda message: True)
def reply_crypto_price(message):
    global robot_active

    text = message.text.lower()

    if text == "روشن!":
        robot_active = True
        bot.reply_to(message, "✅ ربات روشن شد.")
        return
    elif text == "خاموش!":
        robot_active = False
        bot.reply_to(message, "❌ ربات خاموش شد.")
        return
    if not robot_active:
        return
    for name, symbol in crypto_list.items():
        if name in text:
            usdt_price = get_usdt_price()
            if not usdt_price:
                bot.reply_to(message, "❌ خطا در دریافت قیمت تتر!")
                return

            latest, best_sell, best_buy, trend = get_crypto_price(symbol)
            if latest:
                price_in_usdt = round(latest / usdt_price, 4)
                response_text = (
                    f"💰 **قیمت لحظه‌ای {name.upper()}:** {latest} تومان (~{price_in_usdt} USDT)\n"
                    f"📈 **بالاترین:** {best_sell} تومان\n"
                    f"📉 **کمترین:** {best_buy} تومان\n"
                    f"📊 **روند:** {trend}\n\n"
                    f"[👨‍💻 ساخته شده توسط مستر شایان](https://t.me/MasterShayan)"
                )
                bot.reply_to(message, response_text, parse_mode="Markdown", disable_web_page_preview=True)
            else:
                bot.reply_to(message, f"❌ خطا در دریافت قیمت {name.upper()}!")
            return

if __name__ == '__main__':
    bot.infinity_polling()
