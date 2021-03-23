## Foothold

1. Run nmap and we get only one port open : 80
2. Website talks about php based terminal.
3. Run gobuster and we get a directory called dev. In dev we can see there are two php files which were similar to the ones in the github repo linked by the creator.
4. Opening anyone we can see that it is a web based terminal already logged in as www-data.
5. We can open a listener and try multiple rev shells.
6. We see ipv6 python one works (from payload of all things)
7. After getting shell we can cat out the user.txt as we don't require user permission to read it.

## PrivEsc

8. Running sudo -l we can see that we can log in(not login but execute commands) as scriptmanager without pass.
9. sudo -u scriptmanager /bin/bash.
10. After running linpeas we can see that /scripts shouldn't be there in the root directory.
11. Two files: test.py and test.txt
12. test.txt is owned by root while we can make changes in test.py
13. When we read contents of test.txt we can see that test.py is writing to test.tx, which means that test.py is running as root as a cronjob (can be checked by changing the text in test.py).
14. Which means, we can take the root.txt directly by changing the test.py : s = open("/root/root.txt","rb").read(); f.write(s).
15. Wait some time and we can see that the change was made.
16. Or we can use the payload (IPv6) one from PayloadOfAllThings and open a listener. 
