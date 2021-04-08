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

- We get a page called balance-transfer which have encrypted usernames and passwords of all the transactions