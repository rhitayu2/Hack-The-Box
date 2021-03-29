## Foothold

1. Run nmap with scripts to check for the open ports. Ports 22 and 80 are open.
2. Robots.txt further gives us many available directories and files present.
3. We can go to /MAINTAINERS.txt and see that it is running version 7.
4. Finding some exploits online or on msfconsole, we can come across this exploit/unix/webapp/drupal_drupalgeddon2 - Drupal Drupalgeddon 2 Forms API Property Injection
5. We can run this to get a shell as apache on the box.

## Priv Esc

6. We can see from this(https://www.drupal.org/forum/support/post-installation/2017-01-13/where-are-the-database-username-and-password-stored) forum that the database username and password are stored in /sites/default/settings.php.
7. We can run mysql -u drupaluser -D drupal -pCQHEy@9M*m23gBVj
8. We can check users and get the password hash for brucetherealadmin. Its encryption mode is Drupal 7.*
9. hashcat -m 7900 pass_hash /opt/SecLists/Passwords/Leaked-Databases/rockyou.txt
10. We get the creds brucetherealadmin:booboo
11. Login using ssh to get a stable shell.
12. Run sudo -l to see that we can run sudo snap install.
13. This means that we need an exploit for snap. Upon googling there are most prominent 2, but we need to use the second variant to get a shell.
14. We should use the payload from the second variant decode in base64 and then write to exploit.snap. Or just run source gen_payload.sh
15. Send it to the box and sudo snap install exploit.snap --dangerous --devmode
16. Our user dirty_sock:dirty_sock would be created.
17. Login as dirty_sock and sudo su, to get the root user, as dirty_sock would be added to the sudoers file
