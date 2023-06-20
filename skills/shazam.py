import asyncio
from shazamio import Shazam
import sounddevice as sd
import soundfile as sf

def record_and_save_audio(duration=7, sample_rate=44100):
    file_path = "/home/leah/Documents/leah-final-hindi/temp/shazam.mp3"
    print(f"Recording {duration} seconds of audio...")

    # Start recording
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait for the recording to complete

    print("Recording completed.")

    # Save audio to file
    sf.write(file_path, audio_data, samplerate=sample_rate, format = 'WAV', subtype = 'PCM_16')
    print(f"Audio saved to '{file_path}'.")
    return file_path

async def recognize_song(file_path):
    shazam = Shazam()
    out = await shazam.recognize_song(file_path)
    return out

def run_song_recognition(file_path):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(recognize_song(file_path))
    if 'track' in result:
        title = result['track']['title']
        artist = result['track']['subtitle']
        print("Title : ", title)
        print("Artist : ", artist)
        return {'title' : title, 'artist' : artist}
    else:
        return {'title' : 'not_found', 'artist' : 'not_found'}

def what_song_is_this(intent_dict):
    tts_object = intent_dict['tts_obj']
    tts_object.text = "play the song now"
    tts_object.play()
    file_path_rec = record_and_save_audio()
    tts_object.text = "please wait, this will take some time"
    tts_object.play()
    song_info = run_song_recognition(file_path=file_path_rec)
    song_tts_metadata = None
    if song_info['title'] == 'not_found' or song_info['artist'] == 'not_found':
        song_tts_metadata = "sorry, I can't find that song"
        print(song_tts_metadata)
        tts_object.text = song_tts_metadata
        tts_object.play()
        return None
    else:
        song_tts_metadata = "its " + song_info['title'] + " by " + song_info['artist']
        print(song_tts_metadata)
        tts_object.text = song_tts_metadata
        tts_object.play()
        return None
