# Enumeration

## Nmap

- Quick Scan
```bash
sudo nmap --max-retries 0 -p- -oN nmap/quick_scan 10.10.10.146                                        130 ↵
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-25 04:15 EDT
Warning: 10.10.10.146 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.146
Host is up (0.18s latency).
Not shown: 65532 filtered ports
PORT    STATE  SERVICE
22/tcp  open   ssh
80/tcp  open   http
443/tcp closed https

Nmap done: 1 IP address (1 host up) scanned in 145.25 seconds

```
- Custom script scan
```bash
sudo nmap -sC -sV -oA nmap/targeted_scan -p 22,80,443 10.10.10.146
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-25 04:18 EDT
Nmap scan report for 10.10.10.146
Host is up (0.18s latency).

PORT    STATE  SERVICE VERSION
22/tcp  open   ssh     OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 22:75:d7:a7:4f:81:a7:af:52:66:e5:27:44:b1:01:5b (RSA)
|   256 2d:63:28:fc:a2:99:c7:d4:35:b9:45:9a:4b:38:f9:c8 (ECDSA)
|_  256 73:cd:a0:5b:84:10:7d:a7:1c:7c:61:1d:f5:54:cf:c4 (ED25519)
80/tcp  open   http    Apache httpd 2.4.6 ((CentOS) PHP/5.4.16)
|_http-server-header: Apache/2.4.6 (CentOS) PHP/5.4.16
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
443/tcp closed https

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 14.79 seconds

```
**Quick Glance**
- Just running a HTTP web server. Apache 2.4.6 - CentOS. PHP based website from the header.

## Website
- Static website
- View-Source:
![[Pasted image 20210425042107.png]]

## Gobuster
```bash
gobuster dir -u http://10.10.10.146 -w $MED_WORD -t 75 -o gb/init_scan -x txt,php    
===============================================================                                                                                                       
Gobuster v3.1.0                                         
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)                                                                                                         
===============================================================                                                                                                       
[+] Url:                     http://10.10.10.146                                                                
[+] Method:                  GET                                                                                
[+] Threads:                 75                                                                                 
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404                                                                                
[+] User Agent:              gobuster/3.1.0                                                                     
[+] Extensions:              txt,php                                                                            
[+] Timeout:                 10s                                                   
===============================================================
2021/04/25 04:22:34 Starting gobuster in directory enumeration mode
===============================================================
/uploads              (Status: 301) [Size: 236] [--> http://10.10.10.146/uploads/]
/index.php            (Status: 200) [Size: 229]
/photos.php           (Status: 200) [Size: 1302]
/upload.php           (Status: 200) [Size: 169]
/lib.php              (Status: 200) [Size: 0]
/backup               (Status: 301) [Size: 235] [--> http://10.10.10.146/backup/]          
Progress: 142434 / 661683 (21.53%)
[!] Keyboard interrupt detected, terminating.                                      

```
- http://10.10.10.146/backup has a tar file containing the source code

