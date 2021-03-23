## Foothold

1. Enumerate the open ports using nmap. We get couple open ports, 21(ftp), 22(ssh), 149 and 445(samba)
2. The vsftpd and the samba versions are vulnerable.
3. Try backdoor vuln for vsftpd, didn't work, probably patched.
4. Try usermap exploit for Samba as the version as 3.0.2 through msfconsole.
5. Works and we get the root user for the box.
6. Thus there is no priv esc part for this box and we can find the root flag in /root directory and the user flag in the makis directory under home.

