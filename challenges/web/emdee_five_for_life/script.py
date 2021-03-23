#!/bin/usr/python3

import requests
import hashlib
import re


req = requests.session()
url = 'http://46.101.15.28:30687/'
rget = req.get(url)
html = rget.content

clean = re.compile('<.*?>')
r = re.sub(clean,'',html.decode())

r2 = r.split('string')[1]
r2 = r2.strip()

mdhash = hashlib.md5(r2.encode()).hexdigest()

data = dict(hash=mdhash)
rpost = req.post(url, data = data)
print(rpost.text)
