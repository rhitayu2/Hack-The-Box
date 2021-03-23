1. enumeration using nmap
2. gobuster gave us the todo.txt, using -x txt
3. from there we could decipher that fergus was a user
4. using cewl and bruteforcing the password
5. password- RolandDeschain
6. Then use the exploit (linux/http/bludit_upload_images_exec) as the 
	host was running an old version of the BLUDIT
7. The vulnerability was we can upload a PHP as GIF or PNG and it wouldnt 
	check, and would update the .htaccess to run the PHP file, which
	can in return run a reverse TCP
8. Or use the exploit in msfconsole and the perl payload was working in 
	as some error in the meterpreter one
9. The password of Hugo stored in MD5 use online decryptor pass-Password120
10. User flag
11. sudo -l gives all root access. Thus run sudo -u#-1 /bin/bash to invoke
	a bash shell as root
12. The flag in /root

