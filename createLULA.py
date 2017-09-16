#!/usr/bin/env python2
"""
Generate 'Locally Assigned Global IDs' according to
RFC 4193 (Proposed Standard).

The Algorithm as decriibed in the RFC:

     1) Obtain the current time of day in 64-bit NTP format [NTP].
     2) Obtain an EUI-64 identifier from the system running this
        algorithm.  If an EUI-64 does not exist, one can be created from
        a 48-bit MAC address as specified in [ADDARCH].  If an EUI-64
        cannot be obtained or created, a suitably unique identifier,
        local to the node, should be used (e.g. system serial number).
     3) Concatenate the time of day with the system-specific identifier
        creating a key.
     4) Compute an SHA-1 digest on the key as specified in [FIPS, SHA1];
        the resulting value is 160 bits.
     5) Use the least significant 40 bits as the Global ID.
     6) Concatenate FC00::/7, the L bit set to 1, and the 40 bit Global
        ID to create a Local IPv6 address prefix.
"""
# Requires Python 2.2 (or better)
from __future__ import generators

__author__ = "Hartmut Goebel <h.goebel@goebel-consult.de>"
__copyright__ = "(c) Copyright 2005 by Hartmut Goebel <h.goebel@goebel-consult.de>"
__version__ = "0.2.1"
__licence__ = "GNU Public Licence (GPL)"

import time
import struct
import commands
import re
import socket
import sha

# from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/117211
TIME1970 = 2208988800L      # Thanks to F.Lundh

def _get_time_ntpformat():
    """
    Get current time of day in 64-bit NTP format.
    """
    # Do not rely on this as being a correct implementation!
    t = time.time() + TIME1970
    # max. 9 decimal-digits fit (always) into 32 bit
    #  10**9  = 1000000000
    #   2**32 = 4294967296
    #  10**10 = 10000000000
    ts = ('%.9f' % t).split('.') # split integer part / fraction part
    ts = map(long, ts) # convert parts to integers
    t = struct.pack('>LL', *ts)
    return t

def _get_EUI64():
    '''
    Create an EUI-64 identifier form the MAC address
    according to "Encapsulated MAC-48 values" in
    http://standards.ieee.org/regauth/oui/tutorials/EUI64.html
    '''
    # get the MAC of some interface
    t = commands.getoutput('/sbin/ip -f link addr show')
    mac = re.findall('link/ether (\S+)', t)[0]
    mac = mac.split(':')
    # insert 'fffe'
    mac[3:3] = ['ff', 'fe']
    mac = map(lambda x: chr(int(x, 16)), mac)
    return ''.join(mac)


def calc_LAGID():
    """
    Calculate a single 'Locally Assigned Global ID' according to
    the algorithm described above.
    """
    # 1) current time of day in 64-bit NTP format 
    t = _get_time_ntpformat();   assert len(t        ) * 8 == 64
    # 2) an EUI-64 identifier from the system running this algorithm
    eui64 = _get_EUI64();        assert len(eui64    ) * 8 == 64
    # 3) Concatenate
    key = t + eui64;             assert len(key      ) * 8 == 128
    # 4) Compute an SHA-1 digest on the key 
    digest = sha.sha(key).digest()
    # 5) least significant 40 bits 
    global_id = digest[-5:];     assert len(global_id) * 8 == 40
    # 6) Concatenate FC00::/7, the L bit set to 1, and global_id
    # fc00::/7 plus L bit set -> fd00::
    prefix = '\xfd' + global_id; assert len(prefix   ) * 8 == 48
    packed = prefix + '\0'* 10;  assert len(packed   ) * 8 == 128
    return packed


def calc_multiple_LAGIDs(num=10):
    """
    Calculate several 'Locally Assigned Global IDs' at once. A ramdom
    delay (up to 1 second) is put between calculations to decrease
    depentences between the generated values.

    This is usefull for getting severl LAG-IDs to select a 'nice' one.
    (Well, this may not be in the sence of the draft ;-)

    num : Number of LAG-IDs to generate
    """
    import random
    for i in range(num):
        prefix = calc_LAGID()
        yield prefix
        time.sleep(random.random())


def asString(prefix):
    """
    Convert a LAG-ID into a string representation (IPv6 address
    format).
    """
    return socket.inet_ntop(socket.AF_INET6, prefix)


def _main():
    for prefix in calc_multiple_LAGIDs(10):
        print "Your 'Locally Assigned Global ID' is",
        print "%s/48" % asString(prefix)
    

if __name__ == '__main__':
    _main()
