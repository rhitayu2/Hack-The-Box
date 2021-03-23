import requests
import ssl

def main():
    url = "http://10.10.10.60/"
    directory = open("./gb/valid_index", "r").read()
    dir_array = directory.split('\n')
    for path in dir_array:
        r = requests.get(url+path, verify=ssl.CERT_NONE)
    print(r.text)

main()
