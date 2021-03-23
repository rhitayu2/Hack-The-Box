nmap to see open ports as ssh and http running on Ubuntu 
enumerate to find login page, inspect element to find the username and password. ash:H@v3_fun
These are the credentials for the system
Fuzz furthermore to find out a virtual host : hms.htb
hms.htb hosted openemr system, OpenSource
Vulnerabilities involve sqli on /portal
use sqlmap to get tables
we can see user as open_emr and password hash. Use hashcat to decrypt password:xxxxxx
Use the exploit in the folder to invoke a netcat client from the open_emr system while opening a listening shell
same invoke a shell, user.txt in /home/ash
See the memcached server on 11211. We dump the items of 1 and all its items: stats cachedum 1 0
Items 2 and 3 contain the username and password for luffy. luffy:0n3_p1ec3
From GTFO bin get the docker command to privelege escalation and from there we can get root_flag at /root : docker run -v /:/mnt --rm -it ubuntu chroot /mnt sh
