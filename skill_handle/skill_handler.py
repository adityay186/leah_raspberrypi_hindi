import sys
sys.path.append("/home/leah/Documents/leah-final-hindi/")
sys.path.append("/home/leah/Documents/leah-final-hindi/tts_engine")

from skills import weather
from skills import time
from skills import search
from skills import news
from skills import send_message
from skills import shazam
from skills import cron_quotes
from skills import sick
from skills import music
from skills import facts

# Mapping of intent types to corresponding skill functions
intent_handlers = {
    'weather': weather.get_weather,
    'time' : time.get_time,
    'search_summary' : search.searchSummary,
    'news' : news.playNews,
    'send_message' : send_message.send_message,
    'song_recognise' : shazam.what_song_is_this,
    'daily_quotes' : cron_quotes.flip,
    'be_a_doctor' : sick.predict_disease,
    'play_music' : music.play_preview_from_query,
    'get_facts' : facts.get_random_fact
    # Add more intent types and corresponding handlers as needed
}

def process_intent(intent):
    intent_type = intent.get('intent_type')
    if intent_type in intent_handlers:
        # Call the corresponding handler function based on intent_type
        res = intent_handlers[intent_type](intent)
        return res
    else:
        # Default handler for unknown intent types
        print("Unknown intent type")
        return " "
