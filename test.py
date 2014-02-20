from ctypes import string_at
from sys import getsizeof
from binascii import hexlify
a = 0x05A0AE14 
print(hexlify(string_at(id(a), getsizeof(a))))