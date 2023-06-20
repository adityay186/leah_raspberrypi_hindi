import datetime
import random

def get_time(time_intent):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%I %M %p")
    prefix_options = ["the time is ", "its "]
    response = random.choice(prefix_options)
    final_string = response + formatted_time
    return final_string
