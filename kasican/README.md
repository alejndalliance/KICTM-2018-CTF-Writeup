## kasican

**Category:** bin

**Points:** -

**Solves:** -

**Description:** -

### Write-up

This binary not supposed to release on that day, its for student category, but i will put the writeup here too because we have the file

this binary should be straight forward. its actually xor encryption.

just find the exncrypted bytes and its key

```asm
movsx   eax, word_432004 ; 0xD1EE
mov     ecx, [ebp+var_30]
movsx   edx, word_432008[ecx*2] ; the bytes array
xor     edx, eax
mov     eax, [ebp+var_30]
mov     word_432008[eax*2], dx
jmp     short loc_4011D6
```
word_432004 => the key (0xD1EE)

word_432008[ecx*2] => the encrypted bytes (BAB98BF188BD8FB6CEB89DF19DE083A182E28B89DDE2AEAB97E0DCE2AEBA87B29ABCCEEBC7F1)

xor this two will get the flag

The flag is s1mpl3eX33@zy123@kictm :) 
