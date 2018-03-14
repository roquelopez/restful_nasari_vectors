#-*- coding: UTF-8 -*-

import requests
#Examples of usage
vector = requests.get('http://localhost:5000/nasari/vector?key=bn:00000003n').json()
print vector

similarity = requests.get('http://localhost:5000/nasari/cosine?key1=bn:00000003n&key2=bn:00000002n').json()
print similarity