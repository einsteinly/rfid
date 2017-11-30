#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import time
import signal

keys = [ [ 0xff, 0xff, 0xff, 0xff, 0xff, 0xff ], [ 0xa0, 0xb0, 0xc0, 0xd0, 0xe0, 0xf0 ], [ 0xa1, 0xb1, 0xc1, 0xd1, 0xe1, 0xf1 ], [ 0xa0, 0xa1, 0xa2, 0xa3, 0xa4, 0xa5 ], [ 0xb0, 0xb1, 0xb2, 0xb3, 0xb4, 0xb5 ], [ 0x4d, 0x3a, 0x99, 0xc3, 0x51, 0xdd ], [ 0x1a, 0x98, 0x2c, 0x7e, 0x45, 0x9a ], [ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 ], [ 0xd3, 0xf7, 0xd3, 0xf7, 0xd3, 0xf7 ], [ 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff ] ]

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

ind = 0
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
    
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        print("\nAuthorizing using key " + str(keys[ind]))
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, keys[ind], uid)

        ind = ind + 1
        if ind >= 8:
          ind = 0

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        else:
            print "Authentication error"

        time.sleep(3)

