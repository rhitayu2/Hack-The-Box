# Enumeration

## Nmap

#### Stage 1: Quick Scan to see all the open ports

```bash
sudo nmap --max-retries 0 -p- 10.10.10.227                                   130 ↵
[sudo] password for norman: 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-02 17:57 EDT
Unable to split netmask from target expression: "nmap/quick_scan"
Warning: 10.10.10.227 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.227
Host is up (0.17s latency).
Not shown: 64313 closed ports, 1220 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
8080/tcp open  http-proxy 

```

#### Stage 2 : Targeted Scan

- We can run custom scripts and enumerate versions on the open ports
```bash
sudo nmap -sC -sV -p 22,8080 -oA nmap/targeted_scan 10.10.10.227
# Nmap 7.91 scan initiated Fri Apr  2 17:58:46 2021 as: nmap -sC -sV -p 22,8080 -oA nmap/targeted_scan 10.10.10.227
Nmap scan report for 10.10.10.227
Host is up (0.17s latency).

PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 6d:fc:68:e2:da:5e:80:df:bc:d0:45:f5:29:db:04:ee (RSA)
|   256 7a:c9:83:7e:13:cb:c3:f9:59:1e:53:21:ab:19:76:ab (ECDSA)
|_  256 17:6b:c3:a8:fc:5d:36:08:a1:40:89:d2:f4:0a:c6:46 (ED25519)
8080/tcp open  http    Apache Tomcat 9.0.38
|_http-title: Parse YAML
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri Apr  2 17:59:02 2021 -- 1 IP address (1 host up) scanned in 16.38 seconds

```

## Gobuster
- We can run gobuster but we can see that there are no useful websites to list (% being a bad character). 
```bash
/test                 (Status: 302) [Size: 0] [--> /test/]
/manager              (Status: 302) [Size: 0] [--> /manager/]
/http%3A%2F%2Fwww     (Status: 400) [Size: 804]
/http%3A%2F%2Fyoutube (Status: 400) [Size: 804]
/http%3A%2F%2Fblogs   (Status: 400) [Size: 804]
/http%3A%2F%2Fblog    (Status: 400) [Size: 804]
/**http%3A%2F%2Fwww   (Status: 400) [Size: 804]
/yaml                 (Status: 302) [Size: 0] [--> /yaml/]
/External%5CX-News    (Status: 400) [Size: 795]
/http%3A%2F%2Fcommunity (Status: 400) [Size: 804]
/http%3A%2F%2Fradar   (Status: 400) [Size: 804]
/http%3A%2F%2Fjeremiahgrossman (Status: 400) [Size: 804]
/http%3A%2F%2Fweblog  (Status: 400) [Size: 804]
/http%3A%2F%2Fswik    (Status: 400) [Size: 804]
```
- The manager directory is password protected, and yaml has the same source code as the base directory of the web page.
- We can enumerate to invalid webpages to see that the tomcat server is hosting a J2EE web application.