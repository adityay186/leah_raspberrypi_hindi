import time
import socket
from mpg123_player import play_mpg123

def check_internet_connection():
    while True:
        try:
            # Attempt to create a socket and connect to www.google.com
            socket.create_connection(("www.google.com", 80))
            print("Connected to the internet.")
            play_mpg123("/home/leah/Documents/leah-final-hindi/tools/connected_successfully.mp3")
            break  # Break out of the loop if connection is successful
        except OSError:
            print("No internet connection. Retrying in 5 seconds...")
            play_mpg123("/home/leah/Documents/leah-final-hindi/tools/no_internet.mp3")
            time.sleep(5)  # Wait for 5 seconds before retrying
