# Enumeration

## Nmap

### Stage 1 : Quick Scan

``` bash
sudo nmap --max-retries 0 -p- $(cat info) -oA nmap/quick_scan         
Nmap scan report for 10.10.10.204                     
Host is up (0.18s latency).                 
Not shown: 65529 filtered ports                         
PORT      STATE SERVICE                           
135/tcp   open  msrpc                           
5985/tcp  open  wsman                      
8080/tcp  open  http-proxy                          
29817/tcp open  unknown                         
29819/tcp open  unknown                         
29820/tcp open  unknown             
Nmap done: 1 IP address (1 host up) scanned in 116.47 seconds                                                         

```

### Stage 2 : Targeted Scan on the open Ports
Grep out all the valid ports to scan from : 
```bash 
cat nmap/quick_scan.nmap| grep open | awk -F/ '{print $1}'  ORS=','
135,5985,8080,29817,29819,29820,
```

Then scan all the ports against default NSE scripts and enumerate versions:

```bash
sudo nmap -sC -sV -oA nmap/targeted_scan $(cat info) -p 135,5985,8080,29817,29819,29820

PORT      STATE SERVICE  VERSION
135/tcp   open  msrpc    Microsoft Windows RPC
5985/tcp  open  upnp     Microsoft IIS httpd
8080/tcp  open  upnp     Microsoft IIS httpd
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=Windows Device Portal
|_http-server-header: Microsoft-HTTPAPI/2.0
|_http-title: Site doesn't have a title.
29817/tcp open  unknown
29819/tcp open  arcserve ARCserve Discovery
29820/tcp open  unknown
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at 

...[snip]...

Nmap done: 1 IP address (1 host up) scanned in 81.74 seconds

```

- Port 5985(??) and 8080 are running web server - Microsoft IIS. 


## Gobuster

## 

### Gobuster against port 5985

```bash
gobuster dir -u http://10.10.10.204:5985 -w $MED_WORD -t 50 -o gb/5985_scan                                [51/81]

...[snip]...

/%C0                  (Status: 400) [Size: 324]
Progress: 107962 / 220561 (48.95%)           
                                                
```

- Interestingly gave us % as a bad character. We can fuzz that further.
```bash
gobuster dir -u http://10.10.10.204:5985 -w /opt/SecLists/Fuzzing/special-chars.txt -o gb/5985_special_chars  1 ↵ 

...[snip]...

[ERROR] 2021/03/28 22:35:28 [!] parse "http://10.10.10.204:5985/%": invalid URL escape "%"

```
- Didn't give much, further fuzzing upon %.