# Privilege Escalation

- We are currently www-data, we can cat out /home/chris/user.txt
- When we traverse backwards, we can see interesting directory in /var --> /var/htb
- There is a binary which is owned by root:root and can be executed by us.
- Execute and it asks are we sure we want get root shell \[y/n\]
- Press y and we can get rootshell. Cat out the root.txt