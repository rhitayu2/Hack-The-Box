# Enumeration 

## Nmap

#### Stage 1 : Custom Script and Version Enumeration
- Custom script and version scan
```bash
sudo nmap -sC -sV -oA nmap/init_scan 10.10.10.43      
Nmap scan report for 10.10.10.43
Host is up (0.16s latency).
Not shown: 998 filtered ports
PORT    STATE SERVICE  VERSION
80/tcp  open  http     Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
443/tcp open  ssl/http Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=nineveh.htb/organizationName=HackTheBox Ltd/stateOrProvinceName=Athens/countryName=GR
| Not valid before: 2017-07-01T15:03:30
|_Not valid after:  2018-07-01T15:03:30
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1

```

**Quick Glance**
- Just an Apache Web server running on 80 and 443, no other initial attack vectors.
- SSL certificate gives us domain name : nineveh.htb. *Need to add in /etc/hosts* 
- Apache 2.4.18 and OS is Ubuntu. Most probably Ubuntu 16.04.

#### Stage 2 : Nmap All port scan
- All port scan also gave these two ports open only

```bash
sudo nmap --max-retries 0 -p- 10.10.10.43 -oA nmap/all_ports
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-30 01:45 EDT
Warning: 10.10.10.43 giving up on port because retransmission cap hit (0).
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up (0.16s latency).
Not shown: 65533 filtered ports
PORT    STATE SERVICE
80/tcp  open  http
443/tcp open  https

Nmap done: 1 IP address (1 host up) scanned in 124.93 seconds
```

#### Stage 3 : Nmap UDP port scan
- No UDP ports open in top 1000 ports.
```bash
sudo nmap -sU 10.10.10.43 -oA nmap/UDP_port_scan                                                            130 ↵
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-30 01:49 EDT
Stats: 0:01:12 elapsed; 0 hosts completed (1 up), 1 undergoing UDP Scan
UDP Scan Timing: About 43.50% done; ETC: 01:52 (0:01:34 remaining)
Nmap scan report for nineveh.htb (10.10.10.43)
Host is up (0.16s latency).
All 1000 scanned ports on nineveh.htb (10.10.10.43) are open|filtered

Nmap done: 1 IP address (1 host up) scanned in 166.16 seconds

```

## Gobuster
#### Stage 1 : Root Directory

- With -x flag for txt and php as php based website
```bash
 gobuster dir -u https://10.10.10.43 -w $MED_WORD -t 60 -o gb/init_scan -x txt,php -k                              
===============================================================                                                       
Gobuster v3.1.0                                                                                                       
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)                                                         
===============================================================                                                       
[+] Url:                     https://10.10.10.43                                                                      
[+] Method:                  GET                                                                                      
[+] Threads:                 60                                                                                       
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt                             
[+] Negative Status codes:   404                                                                                      
[+] User Agent:              gobuster/3.1.0                                                                           
[+] Extensions:              txt,php                                                                                  
[+] Timeout:                 10s                                                                                      
===============================================================                                                       
2021/03/30 01:50:20 Starting gobuster in directory enumeration mode                                                   
===============================================================                                                       
/db                   (Status: 301) [Size: 309] [--> https://10.10.10.43/db/]
/secure_notes		  (Status: 301)
```

####Stage 2 : Gobuster on /db/
```bash
 gobuster dir -u https://10.10.10.43/db -w $MED_WORD -t 60 -o gb/directory_db -x txt,php,cgi -k                              
===============================================================                                                       
Gobuster v3.1.0                                                                                                       
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)                                                         
===============================================================                                                       
[+] Url:                     https://10.10.10.43/db                                                                      
[+] Method:                  GET                                                                                      
[+] Threads:                 60                                                                                       
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt                             
[+] Negative Status codes:   404                                                                                      
[+] User Agent:              gobuster/3.1.0                                                                           
[+] Extensions:              txt,php,cgi                                                                                 
[+] Timeout:                 10s                                                                                      
===============================================================                                                       
2021/03/30 01:50:20 Starting gobuster in directory enumeration mode                                                   
===============================================================                                                       
/index.php                   (Status: 301) [Size: 309] [--> https://10.10.10.43/db/]                                         
```

#### Stage 3 : Gobuster on port 80 (http://10.10.10.43)
```bash
gobuster dir -u http://10.10.10.43 -w $MED_WORD -t 75 -o gb/http                                   
===============================================================                                        
Gobuster v3.1.0                                                                                        
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.10.43
[+] Method:                  GET
[+] Threads:                 75
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2021/03/31 00:46:49 Starting gobuster in directory enumeration mode
===============================================================
/department           (Status: 301) [Size: 315] [--> http://10.10.10.43/department/]
Progress: 70864 / 220561 (32.13%)                                                  ^C
[!] Keyboard interrupt detected, terminating.
                                                                                     
===============================================================
2021/03/31 00:49:38 Finished                               
===============================================================                                                       
```