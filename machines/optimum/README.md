## Foothold

1. Run nmap and we can see that only 1 port is open : 80.
2. Opening the website we can see that it is a HTTP file server (HFS - 2.3)
3. search hfs in msf console, 1 exploit which shows that we exploit the seqarch parameter, which doesn't sanitize input which can give us RCE.
4. Run that we can get user.txt

## Priv Esc

5. Run post/multi/recon/local_exploit_suggester and we see 2 exploits are available.
6. exploit/windows/local/ms16_032_secondary_logon_handle_privesc will give us the root.txt
