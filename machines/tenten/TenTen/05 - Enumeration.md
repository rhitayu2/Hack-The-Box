# Enumeration

## Nmap

- Quick scan
```bash
sudo nmap --max-retries 0 -p- -oN nmap/quick_scan 10.10.10.10.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-15 03:25 EDT
Warning: 10.10.10.10 giving up on port because retransmission cap hit (0).
Stats: 0:00:57 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 30.61% done; ETC: 03:28 (0:02:09 remaining)
Stats: 0:00:58 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 30.79% done; ETC: 03:28 (0:02:08 remaining)
Nmap scan report for 10.10.10.10. (10.10.10.10)
Host is up (0.17s latency).
Not shown: 65533 filtered ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 147.64 seconds

```
- Custom Scripts and Version Enumeration
```bash
sudo nmap -sC -sV -oA nmap/targeted_scan -p 22,80 10.10.10.10.
Starting Nmap 7.91 ( https://nmap.org ) at 2021-04-15 03:28 EDT
Nmap scan report for 10.10.10.10. (10.10.10.10)
Host is up (0.17s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ec:f7:9d:38:0c:47:6f:f0:13:0f:b9:3b:d4:d6:e3:11 (RSA)
|   256 cc:fe:2d:e2:7f:ef:4d:41:ae:39:0e:91:ed:7e:9d:e7 (ECDSA)
|_  256 8d:b5:83:18:c0:7c:5d:3d:38:df:4b:e1:a4:82:8a:07 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: WordPress 4.7.3
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Job Portal &#8211; Just another WordPress site
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 17.25 seconds

```
**Quick Glance**
- Running ubuntu
- Apache 2.4.18
- Wordpress Website

## Website
### The Rabbit Hole
- In Job Listings we can check check the pentester job where arbitrary file upload is allowed. We can upload a reverse shell and try to execute, but not taking .php files or GIF8a; prepended.

### Intended Method
- We can see that job listings is present in directory : 8.
- We can use curl to enumerate all the Directories from 1-20
```bash
for i in `seq 1 20`;
do
echo -n $i:; curl -s http://10.10.10.10/index.php/jobs/apply/$i/ | grep '<title>'
done

...[snip]...
11:<title>Job Application: cube &#8211; Job Portal</title>
12:<title>Job Application: Application &#8211; Job Portal</title>
13:<title>Job Application: HackerAccessGranted &#8211; Job Portal</title>
14:<title>Job Application: Application &#8211; Job Portal</title>
15:<title>Job Application: Application &#8211; Job Portal</title>
16:<title>Job Application: cmd &#8211; Job Portal</title>
...[snip]...
```
- We can see there is a file called HackerAccessGranted.
- All files are stored in http://\<website\>/\<wordpress\>/wp-content/uploads/\<year\>/\<month\>/\<filename\>
- I have written a python script to enumerate sequentially.
```bash
python3 exploit.py 
[*] Trying: http://10.10.10.10/wp-content/uploads/2017/04/HackerAccessGranted.jpg
[+] Found: http://10.10.10.10/wp-content/uploads/2017/04/HackerAccessGranted.jpg
[!] Done

```
- We can see that it is an image
![[Pasted image 20210415090612.png]]
- We can download it and run steghide against it.
```bash
steghide extract -sf HackerAccessGranted.jpg
Enter passphrase: 
wrote extracted data to "id_rsa".

```
- Just press enter on password prompt for blank password.
- It is an encrypted RSA private key
```bash
cat id_rsa                                                                                  
-----BEGIN RSA PRIVATE KEY-----                                                                 
Proc-Type: 4,ENCRYPTED                                                                          
DEK-Info: AES-128-CBC,7265FC656C429769E4C1EEFC618E660C                                          
                                                                                                
/HXcUBOT3JhzblH7uF9Vh7faa76XHIdr/Ch0pDnJunjdmLS/laq1kulQ3/RF/Vax                                
tjTzj/V5hBEcL5GcHv3esrODlS0jhML53lAprkpawfbvwbR+XxFIJuz7zLfd/vDo                                
1KuGrCrRRsipkyae5KiqlC137bmWK9aE/4c5X2yfVTOEeODdW0rAoTzGufWtThZf                                
...[snip]...
```
