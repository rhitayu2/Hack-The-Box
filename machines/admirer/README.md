## Foothold

1. Upon enumerating ports we see that three ports are open 21,22,80
2. FTP doesnt allow anonymous loign.
3. We check the web page. We run gobuster to see that there is a robots.txt which has /admin-dir blacklisted by 'waldo' which is a potential username.
4. Now we can gobuster /admin-dir further and see that there is contacts.txt and credentials.txt. Potential usernames and passwords in credentials.txt.
5. We can login to ftp using credentials found in credentials.txt
6. GET dump.sql and html.tar.gz
7. Few more passwords and directories found in utility-scripts.
8. Run gobuster on utility-scripts directory we get adminer.php.
9. Vulnerability using adminer present. We have to host a local database server on our machine and create a valid user for 10.10.10.187 and then we can login from their portal and dump files in out database.
10. When we login to their portal using credentials created by us, we can use ==> LOAD DATA LOCAL INFILE 'file_name' INTO TABLE our_db.our_table.
11. The above SQL command will dump the contents of the file. But due to base direcctory restriction we can just try to dump the initial index.php and we get new credentials for waldo.
12. Use it login through ssh and cat out the user_flag.


## Priv Esc

13. As we know the password we can run sudo -l we can see what waldo can execute as root.
14. /opt/scripts has two files backup.py and admin_scripts.sh. We see that case 6 executes backup.py which is importing shutil and make_archive function. We can specify local PYTHONPATH to check for the function first and then we can use this to get RCE as sudo.
15. We can create a shutil.py in /dev/shm or /tmp and execute the file as sudo PYTHONPATH=pth_to_shutil_py admin_tasks.sh 6
16. We can cat out the root.txt
