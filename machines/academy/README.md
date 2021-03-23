## Initial

run sudo nmap -sC -sV -oA nmap/init_scan.out 10.10.10.215
We get a redirect for academy.htb
Add academy.htb to /etc/hosts
Open in browser

## Run gobuster on academy.htb
We get admin.htb
To get an admin account go to /register
Capture packet for register
Change roleid to 1 instead of 0
Send packet for creating admin account
Login as admin in /admin.php
We can see 2 other accounts other than egre55
We get a table for a vhost dev-staging-01
Add vhost to /etc/hosts

## Opening Vhost
We get a Laravel framework of PHP
msfconsole has an exploit for this
Put parameters correctly and run exploit
We get a reverseshell for www-data

## Checking valid users
When we check /var/www/academy/.env file, we can see a password
We can check the password for valid users through ssh for all three users
cryolite has the password
check the user.txt

## Priv Esc
Run linpeas.sh
Check /var/log/audit
grep all the 4 files for common="su"
We get a data variable assigned some hex value
Decoding hex value gives us the password for mrb3n(apparent from password)
After logging in as mrb3n, we can check sudo -l
Composer can run as sudo
We check a sudo escape from GTFO bin

## Method 1
root.txt is usually present in /root, thus one script can just read root.txt

## Method 2
Create a ssh-key for logging in and place it in /root/.ssh/authroized_keys
Login through ssh => ssh -i file_name root@10.10.10.215
Password set during keygen
We can get root.txt
