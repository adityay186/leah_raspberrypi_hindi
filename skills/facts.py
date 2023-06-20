import requests

def get_random_fact(intent_dict):
    api_url = 'https://api.api-ninjas.com/v1/facts?limit=1'
    response = requests.get(api_url, headers={'X-Api-Key': 'p4mk5rx4r5PNbnQnfTfRrg==HkPvXY6vLw92tY2z'})

    if response.status_code == requests.codes.ok:
        fact_data = response.json()
        if fact_data:
            fact = fact_data[0]['fact']
            return fact
    else:
        print("Error:", response.status_code, response.text)
    
    return None
