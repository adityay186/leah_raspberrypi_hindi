import requests
import json
import time
import sys
import datetime

sys.path.append("/home/leah/Documents/leah-final-hindi/tools")

from mpg123_player import play_mpg123
from send_message import send_telegram_message

val = None
i = 1

def get_current_datetime():
    current_datetime = datetime.datetime.now()
    
    date_dict = {
        'year': current_datetime.year,
        'month': current_datetime.month,
        'day': current_datetime.day,
        'hour': current_datetime.strftime("%I"),
        'minute': current_datetime.minute,
        'second': current_datetime.second,
        'am_pm': current_datetime.strftime("%p")
    }
    
    return date_dict

def motion():
    global val
    global i
    
    link = "https://api.thingspeak.com/channels/2193643/feeds.json?api_key=22VZF8OP8OGRB66G&results=2"
    
    print("Home Monitor:")

    play_mpg123("/home/leah/Documents/leah-final-hindi/tools/please_wait_home_security.mp3")
    
    while True:
        print("Waiting 5 Seconds..")
        time.sleep(5)
        print("Sending Request..")
        r = requests.get(link)
        data = json.loads(r.text)
        
        if 'last_entry_id' in data['channel']:
            val2 = data['channel']['last_entry_id']
            
            if val is None:
                val = val2
                continue
            
            if val2 == val:
                print(i, "No Detection:", val2)
            else:
                print(i, "Motion Detected:", val2)
                val = val2
                i += 1
                tm = get_current_datetime()
                message_string = "Leah Home Security :\n\nMotion has been detected in your home on *{}/{}/{}* at *{}:{}:{} {}*\n\n*Take Action Immediately\\!* ".format(tm['day'], tm['month'], tm['year'], tm['hour'], tm['minute'], tm['second'], tm['am_pm'])
                send_telegram_message(message_string)
                play_mpg123("/home/leah/Documents/leah-final-hindi/tools/motion_detected.mp3")
                play_mpg123("/home/leah/Documents/leah-final-hindi/tools/burglar_alarm.mp3")
                play_mpg123("/home/leah/Documents/leah-final-hindi/tools/take_action_immedietly.mp3")
                print("Take Action Immediately")
                break

        else:
            print("Error: Could not retrieve data from the API")
            break

motion()

