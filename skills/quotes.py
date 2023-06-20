import requests
import asyncio
import telegram

def get_random_quote():
    response = requests.get("https://api.quotable.io/random")
    if response.status_code == 200:
        quote = response.json()
        content = quote["content"]
        author = quote["author"]
        final_quote = "Daily Quotes By Leah : " + "\n" + "\n" + '"' + content + '"' + "\n" + "\n" + "~" + author
        print(final_quote)
        return final_quote
    else:
        print("Failed to fetch a random quote.")

async def send_telegram_message(message):
    # Set your bot token and chat ID
    bot_token = '6192792234:AAEiAxGK_qweROD-88YgnGWoWyAoahTE9P8'
    chat_id = '-960255198'

    # Create a bot instance
    bot = telegram.Bot(token=bot_token)

    # Send the message
    await bot.send_message(chat_id=chat_id, text=message)

    print("Telegram Message Delivered Successfully..")

quote = get_random_quote()
loop = asyncio.get_event_loop()
loop.run_until_complete(send_telegram_message(quote))
