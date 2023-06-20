import requests
from bs4 import BeautifulSoup
from tts_engine import playdirect

def playNewsHindi():
    # URL of the webpage
    url = 'https://newsonair.gov.in/Podcast.aspx'

    try:
        # Send a GET request to the webpage
        response = requests.get(url)

        # Get the HTML content
        html_content = response.text

        # Create a Beautiful Soup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the span element by its ID
        span_element = soup.find('span', id='ctl00_AddUserControl7_label8')

        # Find the audio element within the span
        audio_element = span_element.find_next('audio')

        # Extract the value of the "audio src" attribute
        audio_src = audio_element['src']

        # Print the "audio src" value
        print(audio_src)

        # Play the audio directly from the extracted URL
        playdirect.PlayDirectFromURL(audio_src).play()

    except KeyboardInterrupt:
        # User pressed Ctrl+C, handle the interruption gracefully
        print("KeyboardInterrupt: Program interrupted by the user.")

    except Exception as e:
        print("An error occurred:", str(e))

def playNewsEnglish():
    # URL of the webpage
    url = 'https://newsonair.gov.in/Podcast.aspx'

    try:
        # Send a GET request to the webpage
        response = requests.get(url)

        # Get the HTML content
        html_content = response.text

        # Create a Beautiful Soup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the span element by its ID
        span_element = soup.find('span', id='ctl00_AddUserControl7_label4')

        # Find the audio element within the span
        audio_element = span_element.find_next('audio')

        # Extract the value of the "audio src" attribute
        audio_src = audio_element['src']

        # Print the "audio src" value
        print(audio_src)

        # Play the audio directly from the extracted URL

        print("Fething and Playing the latest news..")
        playdirect.PlayDirectFromURL(audio_src).play()

    except KeyboardInterrupt:
        # User pressed Ctrl+C, handle the interruption gracefully
        print("KeyboardInterrupt: Program interrupted by the user.")

    except Exception as e:
        print("An error occurred:", str(e))

# Call the function to play the audio from the website
def playNews(intent_dict):
    if 'newsCategory' in intent_dict:
        if intent_dict['newsCategory'] == 'english':
            playNewsEnglish()
        else:
            playNewsHindi()
    else:
        playNewsHindi()