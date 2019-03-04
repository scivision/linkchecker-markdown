import requests

EXC = [requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError]
OKE = requests.exceptions.TooManyRedirects
RETRYCODES = (400, 404, 405, 503)
TIMEOUT = 10
