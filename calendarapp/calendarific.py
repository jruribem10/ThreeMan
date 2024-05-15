import requests

def get_holidays(api_key, country, year, language):
    url = f'https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country}&year={year}&language{language}'
    response = requests.get(url)
    holidays = response.json().get('response', {}).get('holidays', [])
    return holidays
