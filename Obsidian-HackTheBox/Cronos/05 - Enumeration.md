# Enumeration

## Nmap

#### Stage 1 : Quick Scan
- Running a fast scan to just enumerate the open ports, we will not know about the services (can't be sure), but we can know which ports to run against.
```bash
sudo nmap -p- --max-retries 0 10.10.10.13 -oN nmap/quick_scan                                                 1 ↵

...[snip]...

PORT   STATE SERVICE
22/tcp open  ssh
53/tcp open  domain
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 169.22 seconds

```

- We can see that it is running a DNS service and a web server on port 80.

#### Stage 2 : 
- Grep out all the valid ports to scan from : 
```bash 
cat nmap/quick_scan | grep open | awk -F/ '{print $1}' | tr '\n' ','
22,53,80,%
```

- Running targeted scan against the ports:
```bash
sudo nmap -sC -sV -p 22,53,80 -oN nmap/targeted_scan 10.10.10.13 -A                                                     130 ↵
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-29 05:29 EDT
Nmap scan report for 10.10.10.13
Host is up (0.18s latency).
Not shown: 997 filtered ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 18:b9:73:82:6f:26:c7:78:8f:1b:39:88:d8:02:ce:e8 (RSA)
|   256 1a:e6:06:a6:05:0b:bb:41:92:b0:28:bf:7f:e5:96:3b (ECDSA)
|_  256 1a:0e:e7:ba:00:cc:02:01:04:cd:a3:a9:3f:5e:22:20 (ED25519)
53/tcp open  domain  ISC BIND 9.10.3-P4 (Ubuntu Linux)
| dns-nsid: 
|_  bind.version: 9.10.3-P4-Ubuntu
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 4.11 (92%), Linux 3.12 (92%), Linux 3.13 (92%), Linux 3.13 or 4.2 (92%), Linux 3.16 (92%), Linux 3.16 - 4.6 (92%), Linux 3.2 - 4.9 (92%), Linux 3.8 - 3.11 (92%), Linux 4.2 (92%), Linux 4.4 (92%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   184.59 ms 10.10.14.1
2   184.71 ms 10.10.10.13

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.01 seconds

```

- DNS Name server DIentifier service is running on port 53 and it is TCP not UDP.
- For now visiting port 80 for further attack vectors

## Dig
- We know that DNS NSID is running.
- Add cronos.htb to /etc/hosts
- Then use axfr to enumerate the VHOSTS. axfr helps us enumerating as it queries for the VHSOST recursively
```bash 
dig axfr cronos.htb @10.10.10.13

; <<>> DiG 9.16.12-Debian <<>> axfr cronos.htb @10.10.10.13
;; global options: +cmd
cronos.htb.             604800  IN      SOA     cronos.htb. admin.cronos.htb. 3 604800 86400 2419200 604800
cronos.htb.             604800  IN      NS      ns1.cronos.htb.
cronos.htb.             604800  IN      A       10.10.10.13
admin.cronos.htb.       604800  IN      A       10.10.10.13
ns1.cronos.htb.         604800  IN      A       10.10.10.13
www.cronos.htb.         604800  IN      A       10.10.10.13
cronos.htb.             604800  IN      SOA     cronos.htb. admin.cronos.htb. 3 604800 86400 2419200 604800
;; Query time: 180 msec
;; SERVER: 10.10.10.13#53(10.10.10.13)
;; WHEN: Mon Mar 29 05:39:58 EDT 2021
;; XFR size: 7 records (messages 1, bytes 203)

```


## Gobuster
- Running gobuster against cronos.htb
```bash
gobuster dir -u http://cronos.htb -w $MED_WORD -t 50 -o gb/init_scan -x txt                                   1 ↵ 

...[snip]...

===============================================================              
2021/03/29 05:40:48 Starting gobuster in directory enumeration mode          
===============================================================                                                                           
/css                  (Status: 301) [Size: 306] [--> http://cronos.htb/css/] 
/js                   (Status: 301) [Size: 305] [--> http://cronos.htb/js/]                                                               
/robots.txt           (Status: 200) [Size: 24]                                                                                            
/server-status        (Status: 403) [Size: 298]                                                                                           
Progress: 234368 / 441122 (53.13%)                                         ^C                                                             
```
- No luck
- Running against http://admin.cronos.htb
```bash
gobuster dir -u http://admin.cronos.htb -w $MED_WORD -t 50 -o gb/admin -x php                              [5/297]
...[snip]...
===============================================================
2021/03/29 06:01:56 Starting gobuster in directory enumeration mode
===============================================================
/index.php            (Status: 200) [Size: 1547]
/welcome.php          (Status: 302) [Size: 439] [--> index.php]
/logout.php           (Status: 302) [Size: 0] [--> index.php]  
/config.php           (Status: 200) [Size: 0]                   
/session.php          (Status: 302) [Size: 0] [--> index.php]  
Progress: 89084 / 441122 (20.19%)                             ^C

```