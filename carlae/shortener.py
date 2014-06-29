# -*- coding: utf-8 -*-

__author__ = 'aobrien'

import math
# SRC: http://kvz.io/blog/2009/06/10/create-short-ids-with-php-like-youtube-or-tinyurl/
ALPHABET = "bcdfghjkmnpqrstvwxyz0123456789BCDFGHJKLMNPQRSTVWXYZ"  # no vowels, no l
BASE = len(ALPHABET)
MINLEN = 2  # at least 1e10 combinations possible with 6 digits

def encode_id(n):

    pad = MINLEN - 1
    n = int(n + pow(BASE, pad))

    s = []
    t = int(math.log(n, BASE))
    while True:
        bcp = int(pow(BASE, t))
        a = int(n / bcp) % BASE
        s.append(ALPHABET[a:a+1])
        n = n - (a * bcp)
        t -= 1
        if t < 0: break

    return "".join(reversed(s))

def decode_id(n):

    n = "".join(reversed(n))
    s = 0
    l = len(n) - 1
    t = 0
    while True:
        bcpow = int(pow(BASE, l - t))
        s = s + ALPHABET.index(n[t:t+1]) * bcpow
        t += 1
        if t > l: break

    pad = MINLEN - 1
    s = int(s - pow(BASE, pad))

    return int(s)

#
#
# import math
# import hashlib
#
# ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#
# def alphaID(idnum, to_num=False, pad_up=False, passkey=None):
#   index = ALPHABET
#   if passkey:
#     i = list(index)
#     passhash = hashlib.sha256(passkey).hexdigest()
#     passhash = hashlib.sha512(passkey).hexdigest() if len(passhash) < len(index) else passhash
#     p = list(passhash)[0:len(index)]
#     index = ''.join(zip(*sorted(zip(p,i)))[1])
#
#   base = len(index)
#
#   if to_num:
#     idnum = idnum[::-1]
#     out = 0
#     length = len(idnum) -1
#     t = 0
#     while True:
#       bcpow = int(pow(base, length - t))
#       out = out + index.index(idnum[t:t+1]) * bcpow
#       t += 1
#       if t > length: break
#
#     if pad_up:
#       pad_up -= 1
#       if pad_up > 0:
#         out -= int(pow(base, pad_up))
#   else:
#     if pad_up:
#       pad_up -= 1
#       if pad_up > 0:
#         idnum += int(pow(base, pad_up))
#
#     out = []
#     t = int(math.log(idnum, base))
#     while True:
#       bcp = int(pow(base, t))
#       a = int(idnum / bcp) % base
#       out.append(index[a:a+1])
#       idnum = idnum - (a * bcp)
#       t -= 1
#       if t < 0: break
#
#     out = ''.join(out[::-1])
#
#   return out
