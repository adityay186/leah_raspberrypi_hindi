import requests
import speech_recognition as sr

tts_obj = None
sr_obj = None

def get_stt():
    tts_obj.text = "what is the message?"
    tts_obj.play()

    stt = None

    with sr.Microphone() as source:
        print("speak the message .. ")
        audio = sr_obj.listen(source, phrase_time_limit=5)
    try:
        stt = sr_obj.recognize_google(audio)
        print(stt)
        return stt
    except sr.UnknownValueError:
        er = "sorry could not recognize"
        tts_obj.text = er
        print(er)
        tts_obj.play()
        return er
    except sr.RequestError as e:
        er2 = "could not fetch results"
        tts_obj.text = er2
        print(er2)
        tts_obj.play()
        return er2

def send_telegram_message(message):
    # Set your bot token and chat ID
    bot_token = '6192792234:AAEiAxGK_qweROD-88YgnGWoWyAoahTE9P8'
    chat_id = '-960255198'

    # Set the Telegram API URL
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    # Set the request parameters
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'MarkdownV2'
    }

    # Send the request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print("Telegram Message Delivered Successfully.")
    else:
        print("Failed to deliver Telegram message.")

    # Print the response content (for debugging purposes)
    print(response.text)

def send_message(entities):
    global tts_obj
    tts_obj = entities['tts_obj']
    global sr_obj
    sr_obj = entities['sr_obj']

    if 'sendMessageCategory' in entities:
        if entities['sendMessageCategory'] == 'telegram':
            message = get_stt()
            send_telegram_message(message)
            return "message sent successfully"

