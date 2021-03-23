## Foothold

1. By running nmap scan we can see that onyl two ports are open : 22, 80.
2. Also by enumeration we can see that this is an OpenBSD box. 
3. Opening the web-page we can see that there is a login page, we can try sql injection.
4. Was unsuccesful, therefore enumerated more, ran gobuster and saw there is a directory named as includes, where two files called as auth.php and auth.php.swp. Upon opening the latter we can see that there is a file which is checking the username and password as its two arguments and we can see the server side code, which takes username as a session variable. 
5. The binary used for checking is located in /auth_helpers/check_auth. Curl this file and we cannot run it, didn't try much running it. File gave us the information that it isn't stripped, therefore used strings to just checkif some credentials are there. Saw that a function auth_userokay is being used also ldd gave a hint regarding the priv esc and authentication by pass. 
6. Googling auth_userokay and vulns we saw a qualys blog post regarding this. Now we know that the check_auth is taking username and password as the first and second parameter and checking for using auth_userokay. The bug says that we can bypass this in openBSD 6.6 by passing the username as -schallenge.
7. But we still need to come up with a way to specify the proper username for their ssh keys. We can do this by passing username in the cookies. Run the script exploit.py to get the private key.
8. chmod 600 and ssh -i id_rsa jennifer@10.10.10.199

## Priv Esc

9. The whole blog post mentioned many ways to priv esc, we can see this code at https://raw.githubusercontent.com/bcoles/local-exploits/master/CVE-2019-19520/openbsd-authroot.
10. Just mv it to /tmp and run it, will get a shell for user.

## Untested Method

11. Post exploit there was a cgi-bin in www, need to check shell shock
