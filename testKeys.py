#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = False

keys = [ [ 0xff, 0xff, 0xff, 0xff, 0xff, 0xff ], [ 0xa0, 0xb0, 0xc0, 0xd0, 0xe0, 0xf0 ], [ 0xa1, 0xb1, 0xc1, 0xd1, 0xe1, 0xf1 ], [ 0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5 ], [ 0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5 ], [ 0x4d, 0x3a, 0x99, 0xc3, 0x51, 0xdd ], [ 0x1a, 0x98, 0x2c, 0x7e, 0x45, 0x9a ], [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ], [ 0xd3, 0xf7, 0xd3, 0xf7, 0xd3, 0xf7 ], [ 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff ] ]

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    rdr.wait_for_tag()

    (error, data) = rdr.request()
    if not error:
        print("\nDetected: " + format(data, "02x"))

    (error, uid) = rdr.anticoll()
    if not error:
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        print("Setting tag")
        util.set_tag(uid)
        print("\nAuthorizing")
        util.auth(rdr.auth_a, key[0] )

        print("Status: "+ str(status))
        print("\nReading")
        util.read_out(32)
        print("\nDeauthorizing")
        util.deauth()

        print("delaying 3 seconds")
        time.sleep(3)
