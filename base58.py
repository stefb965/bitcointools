#!/usr/bin/env python

"""encode/decode base58 in the same way that Bitcoin does"""

import math

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v):
  """ encode v, which is a little-endian string of bytes, to base58.    
  """

  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += (256**i) * ord(c)

  result = ''
  while long_value >= __b58base:
    div, mod = divmod(long_value, __b58base)
    result = __b58chars[mod] + result
    long_value = div
  result = __b58chars[long_value] + result

  # Pad front with Base58-encoded-0 for leading zeros:
  nPad = int((len(v)*8 / (math.log(58,2))) - len(result))

  return (__b58chars[0]*nPad) + result

try:
  # Python Crypto library is at: http://www.dlitz.net/software/pycrypto/
  # Needed for RIPEMD160 hash function, used to compute
  # Bitcoin addresses from internal public keys.
  from Crypto.Hash import *
  have_crypto = True
except ImportError:
  have_crypto = False

def hash_160(public_key):
  if not have_crypto:
    return ''
  h1 = SHA256.new(public_key).digest()
  h2 = RIPEMD160.new(h1).digest()
  return h2

def public_key_to_bc_address(public_key):
  if not have_crypto:
    return ''
  h160 = hash_160(public_key)
  return hash_160_to_bc_address(h160)

def hash_160_to_bc_address(h160):
  vh160 = "\x00"+h160  # \x00 is version 0
  h3=SHA256.new(SHA256.new(vh160).digest()).digest()
  addr=vh160+h3[0:4]
  return b58encode(addr)

if __name__ == '__main__':
    x = '005cc87f4a3fdfe3a2346b6953267ca867282630d3f9b78e64'.decode('hex_codec')
    print b58encode(x), '19TbMSWwHvnxAKy12iNm3KdbGfzfaMFViT'
