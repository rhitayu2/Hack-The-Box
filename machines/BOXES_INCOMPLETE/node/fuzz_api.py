import requests

DEBUG = 1
RHOST="http://10.10.10.58:3000"
API_WORDLIST="/opt/SecLists/Discovery/Web-Content/api/objects-lowercase.txt"
API_DIRECTORY="/api/"

def main():
    base_file = requests.get("http://10.10.10.58:3000")
    wordlist = open(API_WORDLIST,"r")
    for line in wordlist:
        api_fuzz = line.strip()
        api_text = requests.get(RHOST+API_DIRECTORY+api_fuzz)
        if DEBUG:
            print(f"[!] Trying : {api_fuzz}", end="\r")
        if api_text.text != base_file.text:
            print(f"\n[+] Found :/{api_fuzz}", end="\n")

main()
