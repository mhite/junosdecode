#!/usr/bin/python

#############################################################################
## this lovely script was painfully ported
## by matt hite (mhite@hotmail.com), who knows
## very little perl
##
## original: http://search.cpan.org/dist/Crypt-Juniper/lib/Crypt/Juniper.pm
## requires python 2.7 due to use of dict comprehension
##
## version 1.0
##

import sys
from optparse import OptionParser, OptionGroup

#################################################################
## globals

MAGIC = "$9$"

###################################
## letter families

FAMILY = ["QzF3n6/9CAtpu0O", "B1IREhcSyrleKvMW8LXx", "7N-dVbwsY2g4oaJZGUDj", "iHkq.mPf5T"]
EXTRA = dict()
for x, item in enumerate(FAMILY):
    for c in item:
        EXTRA[c] = 3 - x

###################################
## forward and reverse dictionaries

NUM_ALPHA = [x for x in "".join(FAMILY)]
ALPHA_NUM = {NUM_ALPHA[x]: x for x in range(0, len(NUM_ALPHA))}

###################################
## encoding moduli by position

ENCODING = [[1, 4, 32], [1, 16, 32], [1, 8, 32], [1, 64], [1, 32], [1, 4, 16, 128], [1, 32, 64]]


def _nibble(cref, length):
    nib = cref[0:length]
    rest = cref[length:]
    if len(nib) != length:
        print "Ran out of characters: hit '%s', expecting %s chars" % (nib, length)
        sys.exit(1)
    return nib, rest


def _gap(c1, c2):
    return (ALPHA_NUM[str(c2)] - ALPHA_NUM[str(c1)]) % (len(NUM_ALPHA)) - 1


def _gap_decode(gaps, dec):
    num = 0
    if len(gaps) != len(dec):
        print "Nibble and decode size not the same!"
        sys.exit(1)
    for x in range(0, len(gaps)):
        num += gaps[x] * dec[x]
    return chr(num % 256)


def juniper_decrypt(crypt):
    chars = crypt.split("$9$", 1)[1]
    first, chars = _nibble(chars, 1)
    toss, chars = _nibble(chars, EXTRA[first])
    prev = first
    decrypt = ""
    while chars:
        decode = ENCODING[len(decrypt) % len(ENCODING)]
        nibble, chars = _nibble(chars, len(decode))
        gaps = []
        for i in nibble:
            g = _gap(prev, i)
            prev = i
            gaps += [g]
        decrypt += _gap_decode(gaps, decode)
    return decrypt


def main():
    parser = OptionParser(usage="usage: %prog [options] encrypted_string",
                          version="1.0")

    (options, args) = parser.parse_args()

    # right number of arguments?
    if len(args) < 1:
        parser.error("wrong number of arguments")

    encrypted_string = args[0]
    print "junos password decrypter"
    print "python version by matt hite"
    print "original perl version by kevin brintnall\n"
    print "encrypted version: %s" % encrypted_string
    print "decrypted version: %s" % juniper_decrypt(encrypted_string)

if __name__ == "__main__":
    main()
