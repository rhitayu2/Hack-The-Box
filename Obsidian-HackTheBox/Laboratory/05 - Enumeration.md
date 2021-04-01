# Enumeration

## Nmap

#### Stage 1 : Quick scan of all ports
```bash
sudo nmap -p- --max-retries 0 10.10.10.216 -oN nmap/quick_scan
# Nmap 7.91 scan initiated Thu Apr  1 03:18:10 2021 as: nmap -p- --max-retries 0 -oN nmap/quick_scan 10.10.10.216
Warning: 10.10.10.216 giving up on port because retransmission cap hit (0).
Nmap scan report for 10.10.10.216
Host is up (0.18s latency).
Not shown: 65532 filtered ports
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https

```

#### Stage 2 : Running custom scripts and version enumeration against these ports
- Parsing out the open ports
```bash
cat nmap/quick_scan| grep open | awk -F/ '{print $1}' | tr '\n' ',' | sed 's/,*$//g'
22,80,443%                                                                                                            
```
- Running custom scripts
```bash
sudo nmap -sC -sV -oA nmap/targeted_scan -p 22,80,443 10.10.10.216                                                              [0/47]
[sudo] password for norman:       
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-01 03:25 EDT                                                                           
Nmap scan report for 10.10.10.216                                    
Host is up (0.18s latency).       

PORT    STATE SERVICE  VERSION                                       
22/tcp  open  ssh      OpenSSH 8.2p1 Ubuntu 4ubuntu0.1 (Ubuntu Linux; protocol 2.0)                                                       
| ssh-hostkey:                    
|   3072 25:ba:64:8f:79:9d:5d:95:97:2c:1b:b2:5e:9b:55:0d (RSA)                                                                            
|   256 28:00:89:05:55:f9:a2:ea:3c:7d:70:ea:4d:ea:60:0f (ECDSA)                                                                           
|_  256 77:20:ff:e9:46:c0:68:92:1a:0b:21:29:d1:53:aa:87 (ED25519)                                                                         
80/tcp  open  http     Apache httpd 2.4.41                           
|_http-server-header: Apache/2.4.41 (Ubuntu)                         
|_http-title: Did not follow redirect to https://laboratory.htb/                                                                          
443/tcp open  ssl/http Apache httpd 2.4.41 ((Ubuntu))                
|_http-server-header: Apache/2.4.41 (Ubuntu)                         
|_http-title: The Laboratory      
| ssl-cert: Subject: commonName=laboratory.htb                       
| Subject Alternative Name: DNS:git.laboratory.htb                   
| Not valid before: 2020-07-05T10:39:28                              
|_Not valid after:  2024-03-03T10:39:28                              
| tls-alpn:                       
|_  http/1.1                      
Service Info: Host: laboratory.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel                                                             

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .                                            
Nmap done: 1 IP address (1 host up) scanned in 23.23 seconds                                                                              
```

**Quick Glance**
- HTTP port 80 redirects to https://laboratory.htb, need to add that in /etc/hosts.
- SSL certificate also provides us with an alternative name : git.laboratory.htb
- No other ports open, we can leave all port scan at the background

## Visiting Website

- laboratory.htb seems like can't be enumerated much
- We can check git.laboratory.htb, create a user, and we can see the version of gitlab is 12.8.1.
- 

