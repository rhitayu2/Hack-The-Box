
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

