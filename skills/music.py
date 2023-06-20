import asyncio
from shazamio import Shazam
import sys

sys.path.append("/home/leah/Documents/leah-final-hindi/tts_engine")

from playdirect import PlayDirectFromURL

async def search_track_and_get_preview_url(query):
    try:
        shazam = Shazam()
        tracks = await shazam.search_track(query=query, limit=1)
        previewurl = tracks['tracks']['hits'][0]['stores']['apple']['previewurl']
        artist_name = tracks['tracks']['hits'][0]['heading']['subtitle']

        return previewurl, artist_name
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None


def play_preview_from_query(intent_dict):
    try:
        query = intent_dict['song_name']
        loop = asyncio.get_event_loop()
        preview_url, artist_name = loop.run_until_complete(search_track_and_get_preview_url(query))
        if preview_url:
            print(f"Artist Name: {artist_name}")
            PlayDirectFromURL(preview_url).play()
        else:
            print("No preview URL found for the given query.")
    
    except KeyboardInterrupt:
        # User pressed Ctrl+C, handle the interruption gracefully
        print("KeyboardInterrupt: Program interrupted by the user.")

    except Exception as e:
        print("An error occurred:", str(e))