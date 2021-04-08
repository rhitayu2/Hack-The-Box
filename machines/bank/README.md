# Loot


## Box Info
- Name : Bank
- IP : 10.10.10.29
- Level : Easy

## Creds

| Service | Username | Password | Description |
| --- | --- | --- | ---| 
| Login Creds | chris@bank.htb | !##HTBB4nkP4ssw0rd!## | Found in /balance-transfers |
# Enumeration

## Nmap

#### Quick Scan
```bash
sudo nmap --max-retries 0 -p- 10.10.10.29 -oN nmap/quick_scan                                130 ↵
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-08 03:15 EDT
Warning: 10.10.10.29 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.29
Host is up (0.19s latency).
Not shown: 61470 closed ports, 4062 filtered ports
PORT   STATE SERVICE
22/tcp open  ssh
53/tcp open  domain
80/tcp open  http

```

#### Targeted Scan
- Enumerating ports
```bash
cat nmap/quick_scan | grep open | awk -F/ '{print $1}' ORS=','
22,53,80,
```
- Custom scripts and version enumeration
```bash
sudo nmap -sC -sV -p 22,53,80 10.10.10.29 -oA nmap/targeted_scan
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-08 03:18 EDT
Nmap scan report for 10.10.10.29
Host is up (0.19s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 08:ee:d0:30:d5:45:e4:59:db:4d:54:a8:dc:5c:ef:15 (DSA)
|   2048 b8:e0:15:48:2d:0d:f0:f1:73:33:b7:81:64:08:4a:91 (RSA)
|   256 a0:4c:94:d1:7b:6e:a8:fd:07:fe:11:eb:88:d5:16:65 (ECDSA)
|_  256 2d:79:44:30:c8:bb:5e:8f:07:cf:5b:72:ef:a1:6d:67 (ED25519)
53/tcp open  domain  ISC BIND 9.9.5-3ubuntu0.14 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.9.5-3ubuntu0.14-Ubuntu
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 18.39 seconds

```

**Quick Glance**
- DNS TCP open, can use dig for zone transferring
- Apache 2.4.7 - Ubuntu

## Website
![[Pasted image 20210408032039.png]]
- Default apache page, therefore virtual hosts must be present,  enumerating other hosts using zone transfering.
```bash
dig axfr @10.10.10.29 bank.htb   

; <<>> DiG 9.16.13-Debian <<>> axfr @10.10.10.29 bank.htb
; (1 server found)
;; global options: +cmd
bank.htb.               604800  IN      SOA     bank.htb. chris.bank.htb. 5 604800 86400 2419200 604800
bank.htb.               604800  IN      NS      ns.bank.htb.
bank.htb.               604800  IN      A       10.10.10.29
ns.bank.htb.            604800  IN      A       10.10.10.29
www.bank.htb.           604800  IN      CNAME   bank.htb.
bank.htb.               604800  IN      SOA     bank.htb. chris.bank.htb. 5 604800 86400 2419200 604800
;; Query time: 184 msec
;; SERVER: 10.10.10.29#53(10.10.10.29)
;; WHEN: Thu Apr 08 03:22:27 EDT 2021
;; XFR size: 6 records (messages 1, bytes 171)

```

- New vhosts:
	- chris.bank.htb
	- ns.bank.htb
	- www.bank.htb
- Reloading www.bank.htb gives us new page
![[Pasted image 20210408034851.png]]
- chris.bank.htb gives us the default apache page.

### login.php
- Seems like a PHP based website

## Gobuster
```bash
gobuster dir -u http://bank.htb -w $MED_WORD -t 75 -o gb/bank_htb
/uploads              (Status: 301) [Size: 305] [--> http://bank.htb/uploads/]
/login.php            (Status: 200) [Size: 1974]
/support.php          (Status: 302) [Size: 3291] [--> login.php]
/assets               (Status: 301) [Size: 304] [--> http://bank.htb/assets/]
/index.php            (Status: 302) [Size: 7322] [--> login.php]
/logout.php           (Status: 302) [Size: 0] [--> index.php]
/inc                  (Status: 301) [Size: 301] [--> http://bank.htb/inc/]
/server-status        (Status: 403) [Size: 288]
/balance-transfer     (Status: 301) [Size: 314] [--> http://bank.htb/balance-transfer/]

```

- We get a page called balance-transfer which have encrypted usernames and passwords of all the transactions# Foothold

![[Pasted image 20210408045412.png]]
- We can see most of the files are around size : 585,584,583,582,581
- If we can find an anomaly
```bash
curl http://bank.htb/balance-transfers > bank_transfers
cat balance_transfers | grep -v "584\|585\|582\|583\|581"    
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
 <head>
  <title>Index of /balance-transfer</title>
 </head>
 <body>
<h1>Index of /balance-transfer</h1>
  <table>
   <tr><th valign="top"><img src="/icons/blank.gif" alt="[ICO]"></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr>
   <tr><th colspan="5"><hr></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[PARENTDIR]"></td><td><a href="/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/unknown.gif" alt="[   ]"></td><td><a href="68576f20e9732f1b2edc4df5b8533230.acc">68576f20e9732f1b2edc4df5b8533230.acc</a></td><td align="right">2017-06-15 09:50  </td><td align="right">257 </td><td>&nbsp;</td></tr>
   <tr><th colspan="5"><hr></th></tr>
</table>
<address>Apache/2.4.7 (Ubuntu) Server at bank.htb Port 80</address>
</body></html>
```

- We can see `68576f20e9732f1b2edc4df5b8533230.acc` is around size 257.
`curl http://bank.htb/balance-transfers/68576f20e9732f1b2edc4df5b8533230.acc -o file.txt`
- file.txt has creds of chris.
- Login and go to support.php
- We can upload file, but only accepting image files. In source code, it is mentioned in \[DEBUG\] --> .htb files can be uploaded to be executed as php
- We can renmae our reverseshell to .htb, we can upload and get a reverse shell. Start listener on local machine before hand.
# Privilege Escalation

- We are currently www-data, we can cat out /home/chris/user.txt
- When we traverse backwards, we can see interesting directory in /var --> /var/htb
- There is a binary which is owned by root:root and can be executed by us.
- Execute and it asks are we sure we want get root shell \[y/n\]
- Press y and we can get rootshell. Cat out the root.txt