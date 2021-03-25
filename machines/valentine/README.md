## Foothold
(Had already seen the ippsec video once)

1. Run nmap scan and we get 3 open ports : 22,80,443.
2. We visit the website on both http and https, we get the logo of Heartbleed vulnerability. We can again run nmap --scripts vuln on the target and we can confirm that we have heartbleed vuln.
3. Use this python script (https://gist.github.com/eelsivart/10174134) to get a memory leak. We can check for useful information (everything base64 encoded) Loop this for a few times and we can get a $test string which when decoded seems like a passphrase.
4. Run gobuster too and we can see three open directories, /dev/ encode/ decode. /dev has a hype_key, which is hex encoded. We can decode to ascii to see that it is a private key. hype would be the user similar to id_rsa, the id part specifies the user.
5. Use the key and passphrase to login to hype.

## Priv Esc

6. Run linpeas and we can see a tmux session standing out.
7. The tmux session can be read and written by root and the hype group. This just check the tmux session, we get root as a user. cat out the root flag.
8. ssh-keygen -f valentine on local machine, change private key to 600 and create a folder in root (.ssh/authorized_keys). Paste the pub key in that and chmod 600. Login using ssh if necessary.
9. Other methods of priv esc can be checked using linux-exploit-suggestor. Ubuntu 3.2.0-23-generic is susceptible to dirty cow. Use that exploit to gain root access.
