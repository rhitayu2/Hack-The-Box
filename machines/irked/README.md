## Foothold

1. We can run sudo nmap (IP) -p- --max-tries 0. This will give us all the open ports, then we can run nmap -sC -sV against these ports, this will speed up our process.
2. We get multiple open ports. Notable are 22, 80 and 6697. (SSH, HTTP and IRC server)
3. We can run gobuster against the webpage, but no use.
4. We can login to the iirc server using irssi. We can see that its a version for 3.2.8.1
5. Little googling, we see that there was a trojan version which allowed backdoor to the server. (RCE).
6. We can run msfconsole and select the exploit and payload and we can get user(ircd) on the box

## Priv Esc

7. We have to escalate to djmardov for getting the user.txt from ~djmardov/Documents/. There is another file which we can read called as .backup which hints to 'steg'. Therefore we need a image which can have encrypted file in it.
8. We can download the image from the website. We can run steghide extract -sf irked.jpg -p $(cat .backup | tail -n 1)to get the password for the user djmardov.
9. Get two ssh connections and let one run linpeas, while manually enumerating through the other. We might come across many binaries which will have set uid for root.
10. We will come across viewuser, which when ran outputs the user and tells us that it cannot run /tmp/listuser.
11. We can create our own payload to get root user. We can either make a rev shell or just execute bash as root.
12. echo "bash" >> /tmp/listuser; chmod +x /tmp/listuser; /usr/bin/viewuser
13. We will get root access. We can create a .ssh folder and store our public key (chmod 600) in authorized_keys.
