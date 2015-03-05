import requests
import json

requests.post('http://localhost:8000/events/', data=json.dumps({'event':'interaction.chin', 'params':{'button':1}}))
