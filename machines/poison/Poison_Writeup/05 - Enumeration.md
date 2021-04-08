# Enumeration

## Nmap

- Quick Scan
```bash
sudo nmap --max-retries 0 -p- 10.10.10.84 -oN nmap/quick_scan
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-08 05:41 EDT
Warning: 10.10.10.84 giving up on port because retransmission cap hit (0).
Stats: 0:00:26 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 27.62% done; ETC: 05:42 (0:01:08 remaining)
Nmap scan report for 10.10.10.84
Host is up (0.18s latency).
Not shown: 54329 filtered ports, 11204 closed ports 
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 61.13 seconds

```
- Enumerate ports
```bash
grep open nmap/quick_scan | awk -F/ '{print $1}' ORS=','                                     130 ↵
22,80,
```
- Custom Scripts and version enumeration
```bash
sudo nmap -sC -sV -p 22,80 -oA nmap/targeted_scan 10.10.10.84
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-08 05:46 EDT
Nmap scan report for 10.10.10.84
Host is up (0.17s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2 (FreeBSD 20161230; protocol 2.0)
| ssh-hostkey: 
|   2048 e3:3b:7d:3c:8f:4b:8c:f9:cd:7f:d2:3a:ce:2d:ff:bb (RSA)
|   256 4c:e8:c6:02:bd:fc:83:ff:c9:80:01:54:7d:22:81:72 (ECDSA)
|_  256 0b:8f:d5:71:85:90:13:85:61:8b:eb:34:13:5f:94:3b (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((FreeBSD) PHP/5.6.32)
|_http-server-header: Apache/2.4.29 (FreeBSD) PHP/5.6.32
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
Service Info: OS: FreeBSD; CPE: cpe:/o:freebsd:freebsd

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.88 seconds

```

**Quick Glance**
-  PHP website
-  Free BSD as OS
