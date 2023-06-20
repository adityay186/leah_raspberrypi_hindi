import sys
import pprint
import subprocess
from mtranslate import translate

sys.path.append("/home/leah/Documents/leah-final-hindi/tools")

home_security_file = "/home/leah/Documents/leah-final-hindi/skills/home_security.py"

from color_print import print_green

from mpg123_player import play_mpg123

print_green("WELCOME TO LEAH")
play_mpg123("/home/leah/Documents/leah-final-hindi/wake_word_engine/leah_startup_sound.mp3")

print_green("PLEASE WAIT, SYSTEM IS LOADING..")
play_mpg123("/home/leah/Documents/leah-final-hindi/wake_word_engine/please_wait.mp3")

print_green("IMPORTING REQUIRED LIBRARIES..")
import struct
import pyaudio
import pvporcupine

print_green("IMPORTING MORE LIBRARIES..")
sys.path.append("/home/leah/Documents/leah-final-hindi/tts_engine")
sys.path.append("/home/leah/Documents/leah-final-hindi/intent_engine")
sys.path.append("/home/leah/Documents/leah-final-hindi/skill_handle")

print_green("IMPORTING FUNCTIONS..")
print_green("IMPORTING INTENT ENGINE..")
from intent import get_intent
from skill_handler import process_intent
print_green("IMPORTING TTS ENGINE..")
from googleTTS import GoogleTTS
print_green("IMPORTING SPEECH RECOGNITION..")
import speech_recognition as sr
from playsound import playsound
from check_internet import check_internet_connection

def detect_wake_word():
    print("INITIALIZING WAKE WORD ENGINE..")
    porcupine = None
    pa = None
    audio_stream = None

    keys = {
            "adityay186@gmail.com" : "61LuNHOI0Wkh4yBbrkck+HDV39muOqtQF3oevQE3Xt+DhIuiWzo1zg==",
            "20190802060@dypiu.ac.in" : "Zb5nW42pBDH0wOptYTK1neJ1fyrYWPJZv0T0IfkFQKmzXTlQZuo24w=="
    }

    tts = GoogleTTS("")
    mic = sr.Microphone()

    try:
        porcupine = pvporcupine.create(access_key = keys["adityay186@gmail.com"],
                                        keyword_paths = ["hey_leah-raspberry_pi/hey_leah-raspberry_pi.ppn"])

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)
        
        check_internet_connection()

        print("WAKE WORD ENGINE RUNNING..\n")

        home_security_process = None

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("**********************************************")
                print_green("WAKE WORD DETECTED!\n")
                command = None
                new_sr = sr.Recognizer()
                #print("new recognizer : ", new_sr)
                with mic as source:
                    print("Speak ...... \n")
                    play_mpg123("start_sound.mp3")
                    audio = new_sr.listen(source, phrase_time_limit = 4)
                try:
                    command = new_sr.recognize_google(audio, language="hi-IN")
                    print("USER SAID ----------> ",command)
                    play_mpg123("end_sound.mp3")
                    command = translate(command, "en")
                    print("\n")
                except sr.UnknownValueError:
                    er = "sorry, could not recognize"
                    tts.text = er
                    print(er)
                    tts.play()
                    continue
                except sr.RequestError as e:
                    er2 = "Could not request results"
                    tts.text = er2
                    print(er2)
                    tts.play()
                    continue

                intention = get_intent(command, new_sr, tts)
                print("INTENT RESULT")
                print("       ↓       ")
                pprint.pprint(intention)
                print("\n")
                if intention['intent_type'] == "home_security":
                    if intention['homeSecurityAction'] == "start":
                        if home_security_process is None or home_security_process.poll() is not None:
                            home_security_process = subprocess.Popen(['python', home_security_file])
                        else:
                            print("Home Monitor is already running")
                    else:
                        if home_security_process is not None and home_security_process.poll() is None:
                            home_security_process.terminate()
                            home_security_process.wait()
                            home_security_process = None
                else:
                    res = process_intent(intention)
                    tts.text = res
                    print("Response ----------> ", res)
                    print("\n")
                    tts.play()

                
    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
                pa.terminate()

detect_wake_word()
