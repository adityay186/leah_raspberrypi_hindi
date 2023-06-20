import requests

def get_weather(city):
    api_key = '182a87f539d9bca49af1ae23ac08e611'  # Replace 'YOUR_API_KEY' with your OpenWeatherMap API key
    query = city['location']

    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=metric'
    response = requests.get(url).json()

    try:
        description = response['weather'][0]['description']
        temp = response['main']['temp']
        temp_min = response['main']['temp_min']
        temp_max = response['main']['temp_max']
        name = response['name']

        result = f"In {name}, it's {temp} degrees Celsius and {description}, with a high of {temp_max} and a low of {temp_min}."
    except KeyError:
        result = "Error: Failed to retrieve weather information."

    return result
