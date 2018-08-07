"""
API: https://westus.dev.cognitive.microsoft.com/docs/services/TextAnalytics.V2.0/operations/56f30ceeeda5650db055a3c6
"""

import requests
from pprint import pprint

subscription_key = "23c49a5d4a874b368fbf775aca82a846"
assert subscription_key

text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
assert text_analytics_base_url

language_api_url = text_analytics_base_url + "languages"
sentiment_api_url = text_analytics_base_url + "sentiment"
key_phrase_api_url = text_analytics_base_url + "keyPhrases"

documents = {'documents': [
    {'id': '1', 'language': 'en',
     'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
    {'id': '90', 'language': 'en',
     'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},
    {'id': '3.1', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},
    {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'},
    {'id': '5', 'language': 'en',
     'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
    {'id': '6', 'language': 'en',
     'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},
    {'id': '7', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},
    {'id': '8', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'},
    {'id': '9', 'language': 'en',
     'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
    {'id': '10', 'language': 'en',
     'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},
    {'id': '11', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},
    {'id': '12', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'},
    {'id': '13', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
    {'id': '14', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},
    {'id': '15', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},
    {'id': '16', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]}

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(sentiment_api_url, headers=headers, json=documents)
sentiments = response.json()
pprint(sentiments)

# headers = {"Ocp-Apim-Subscription-Key": subscription_key}
# response = requests.post(key_phrase_api_url, headers=headers, json=documents)
# key_phrases = response.json()
# pprint(key_phrases)
