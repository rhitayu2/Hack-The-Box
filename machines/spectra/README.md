## Foothold

1. Run nmap scan on the site, three ports are open: 22, 80, 3306
2. Visiting the site we get two further directories: /main and /testing
3. /main has a wordpress site hosted on it, where we can see that there is a user login and a possible username of administrator
4. When we enumerate to /testing, php error of database connection not possible.
5. Enumerate further to /wp-admin or such sites, list of pages present. File called wp-config.php.save, which can be read. Found credentials for devtest:devteam01
6. Tried loggin in with those credentials. Tried same password with administrator, worked.
7. A Wordpress site, therefore, we have basic login, can run msf for exploits or mainly plugin, theme editing for 404.php websites or similar websites.
8. Run msf with creds and details. Drop shell.

## Priv Esc

9. Now enumerating using linpeas.sh or any other scripts.
10. We can see the multiple users present in /home
11. We can see that there is a file in /opt/autologin.conf.orig, there is a references to the directories to /mnt/stateful_partition/etc/autologin /etc/autologin.
12. In /etc/login, we can find a password, but don't know the user, we can use the users we found in /home directory, apparently password for katie.
13. We can log in as katie and see the user text.
14. Run sudo -l and see katie can run /sbin/initctl. initctl same as systemctl and it executes script from /etc/init
15. list files in /etc/init and see all the files named test can be edited by us.

### Three methods tried by me

1. cat /root/root.txt > /tmp/some_file
2. cat /root/.ssh/id_rsa > /tmp/some_file
3. chmod +s /bin/bash. Then run /bin/bash -p as katie. 
Method 2 was giving the rsa key, but cannot login through ssh.
