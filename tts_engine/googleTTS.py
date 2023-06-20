from gtts import gTTS
import os
import sys

sys.path.append("/home/leah/Documents/leah-final-hindi/tools")

from mpg123_player import play_mpg123
from mtranslate import translate

class GoogleTTS:
    def __init__(self, text):
        print("::creating gTTS object::")
        self.language = "en"
        self.text = text

    def translate_to_hindi(self):
        self.text = translate(self.text, "hi")

    def play(self):
        if self.text == None or self.text == "" or self.text == " ":
            pass
        else:
            # Translate the text to Hindi
            self.translate_to_hindi()

            print("gtts text : ", self.text)

            try:
                # Create a gTTS object
                tts = gTTS(text=self.text, lang=self.language)

                # Save the speech as an MP3 file
                print("::saving audio::")
                tts.save("tts.mp3")

                # Play the audio using mpg123 player
                print("::Playing TTS:: \n")
                play_mpg123("tts.mp3")
                print("::Done Playing:: \n")

            except Exception as e:
                print("An error occurred:", str(e))
                play_mpg123("something_went_wrong.mp3")

            finally:
                # Remove the temporary audio file
                if os.path.exists("tts.mp3"):
                    os.remove("tts.mp3")

