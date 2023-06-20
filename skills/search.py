import requests

def extract_first_sentence(text):
    # Split the text into sentences using period as the delimiter
    sentences = text.split('. ')
    
    # Extract the first sentence
    first_sentence = sentences[0]
    
    return first_sentence

def searchSummary(query):
    q = query['search_entity']
    url = f"https://api.duckduckgo.com/?q={q}&format=json&pretty=1&no_html=1&skip_disambig=1"
    response = requests.get(url)
    data = response.json()
    
    if 'AbstractText' in data:
        abstract_text = data['AbstractText']
        first_sentence = extract_first_sentence(abstract_text)
        return first_sentence
    else:
        return None