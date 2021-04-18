ng# Enumeration

## Nmap

- Full Scan - Running custom scripts and version enumeration on all ports
```bash
sudo nmap -sC -sV -oA nmap/full_scan 10.10.10.153 -p-                                 130 ↵Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-15 09:32 EDT
Nmap scan report for 10.10.10.153Host is up (0.19s latency).Not shown: 65534 closed ports
PORT   STATE SERVICE VERSION
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
	|_http-server-header: Apache/2.4.25 (Debian)|_http-title: Blackhat highschoolService detection performed. Please 		report any incorrect results at https://nmap.org/submit/ .Nmap done: 1 IP address (1 host up) scanned in 1250.03 seconds

```

**Quick Glance**
- Just Port 80 open
- Apache 2.4.25 and Debian
- Mention of a portal to login. Need to check that - moodle

## Gobuster

### Directory Enumeration
```bash
/images               (Status: 301) [Size: 313] [--> http://10.10.10.153/images/]
/css                  (Status: 301) [Size: 310] [--> http://10.10.10.153/css/]
/manual               (Status: 301) [Size: 313] [--> http://10.10.10.153/manual/]
/js                   (Status: 301) [Size: 309] [--> http://10.10.10.153/js/]
/javascript           (Status: 301) [Size: 317] [--> http://10.10.10.153/javascript/]
/fonts                (Status: 301) [Size: 312] [--> http://10.10.10.153/fonts/]
/phpmyadmin           (Status: 403) [Size: 297]
/moodle               (Status: 301) [Size: 313] [--> http://10.10.10.153/moodle/]
/server-status        (Status: 403) [Size: 300]

```

- In /images, we can see that 5.png has different size than all the other images.
- We can download that and we can check for the contents.
```bash
cat 5.png.1 
Hi Servicedesk,

I forgot the last charachter of my password. The only part I remembered is Th4C00lTheacha.

Could you guys figure out what the last charachter is, or just reset it?

Thanks,
Giovanni

```
- We can see that we need to figure out the last character of the password, considering utf-8 encoding.
- Using the python3 script in the directory - `exploit.py`, we can just bruteforce the password.
- Credentials for loggin in --> giovanni:Th4C00lTheacha#
