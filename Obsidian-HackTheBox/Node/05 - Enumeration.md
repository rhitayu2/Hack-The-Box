# Enumeration

## Nmap

#### Stage 1: Quick All port scan
- Getting all the open TCP ports
```bash
sudo nmap --max-retries 0 -p- 10.10.10.58 -oN nmap/quick_full_scan 
[sudo] password for norman: 
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-30 09:28 EDT
Warning: 10.10.10.58 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.58
Host is up (0.17s latency).
Not shown: 65533 filtered ports
PORT     STATE SERVICE
22/tcp   open  ssh
3000/tcp open  ppp

```

#### Stage 2 : Running custom script and version enumeration

- Running against enumerated ports

 ```bash
cat nmap/quick_full_scan| grep open | awk -F/ '{print $1}' | tr '\n' ','
22,3000,
```

```bash
sudo nmap -sC -sV -oA nmap/targeted_scan -p 22,3000 10.10.10.58                                                   
[sudo] password for norman:                                                                                           
Starting Nmap 7.91 ( https://nmap.org ) at 2021-03-30 10:31 EDT                                                       
Nmap scan report for 10.10.10.58
Host is up (0.17s latency).

PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:5e:34:a6:25:db:43:ec:eb:40:f4:96:7b:8e:d1:da (RSA)
|   256 6c:8e:5e:5f:4f:d5:41:7d:18:95:d1:dc:2e:3f:e5:9c (ECDSA)
|_  256 d8:78:b8:5d:85:ff:ad:7b:e6:e2:b5:da:1e:52:62:36 (ED25519)
3000/tcp open  hadoop-datanode Apache Hadoop
| hadoop-datanode-info: 
|_  Logs: /login
| hadoop-tasktracker-info: 
|_  Logs: /login
|_http-title: MyPlace
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

**Overview**
- Normal SSH port running.
- Currently we can just enumerate port 3000. Apache Hadoop running on it


## Gobuster
- All the directories which don't exist, redirect to homepage, thus prividing 200 status code.
- View source of any web page, we get these pages:
```html
<script type\="text/javascript" src\="[assets/js/app/controllers/home.js](view-source:http://10.10.10.58:3000/assets/js/app/controllers/home.js)"></script\> <script type\="text/javascript" src\="[assets/js/app/controllers/login.js](view-source:http://10.10.10.58:3000/assets/js/app/controllers/login.js)"></script\> <script type\="text/javascript" src\="[assets/js/app/controllers/admin.js](view-source:http://10.10.10.58:3000/assets/js/app/controllers/admin.js)"></script\> <script type\="text/javascript" src\="[assets/js/app/controllers/profile.js](view-source:http://10.10.10.58:3000/assets/js/app/controllers/profile.js)"></script\> <script type\="text/javascript" src\="[assets/js/misc/freelancer.min.js](view-source:http://10.10.10.58:3000/assets/js/misc/freelancer.min.js)"></script\>
```
- Parsing 
```bash
cat pages | awk '{print $3}' | awk -F "\"" '{print $2}'               
assets/js/app/controllers/home.js
assets/js/app/controllers/login.js
assets/js/app/controllers/admin.js
assets/js/app/controllers/profile.js
assets/js/misc/freelancer.min.js
```

## Manual Enumeration

- Also, we can either FUZZ the API points or the box might be intended for manual enumeration from the available files.
- We can check the routes from the file structure of the web page:
![[Pasted image 20210331175343.png]]