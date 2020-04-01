import requests
import random

URL = "https://arunrocks.com/minimal-hugo-site-tutorial/"
URL = URL + "?random=" + str(random.randint)

response = requests.get(URL)

requests.post('http://localhost:8080/api/items', auth=('stuff@kwoh.de', '123456'), json={'url': URL, 'html': response.text})

