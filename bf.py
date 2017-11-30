from pirc522 import RFID
import time
rdr = RFID()

key = [0, 0, 0, 0, 0, 0]
auth_key = [0, 0, 0, 0, 0, 0]
a1 = 255
a2 = 255
a3 = 255
a4 = 255
a5 = 255
a6 = 253

while True:
  
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
#     print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
#       print("UID: " + str(uid))
      # Select Tag is required before Auth
      if not rdr.select_tag(uid):          
        key = [a1, a2, a3, a4, a5, a6]
        print(str(key))
        status = rdr.card_auth(rdr.auth_a, 10, key, uid)
        if not status:
          auth_key = key
          print("authorised key: " + str(auth_key))
          time.sleep(3600000)
        # Auth for block 10 (block 2 of sector 2) using default shipping key A
#         if not rdr.card_auth(rdr.auth_a, 10, auth_key, uid):
#           # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
#           print("Reading block 10: " + str(rdr.read(10)))
#           # Always stop crypto1 when done working
#           rdr.stop_crypto()
        a6 +=1
        if a6 == 256:
          a6 = 0
          a5 += 1
          if a5 == 256:
            a5 = 0
            a4 += 1
            if a4 == 256:
              a4 = 0
              a3 += 1
              if a3 == 256:
                a3 = 0
                a2 += 1
                if a2 == 256:
                  a2 = 0
                  a1 += 1
                  if a1 == 256:
                    a1 = 0

# Calls GPIO cleanup
rdr.cleanup()
