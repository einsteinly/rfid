from pirc522 import RFID
import time
rdr = RFID()

while True:
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UID: " + str(uid))
      # Select Tag is required before Auth
      if not rdr.select_tag(uid):
        key = [0, 0, 0, 0, 0, 0]
        auth_key = [0, 0, 0, 0, 0, 0]
        for a1 in range(256):
          print("epoch " + str(a1+1) + " out of 256")
          for a2 in range(256):
            for a3 in range(256):
              for a4 in range(256):
                for a5 in range(256):
                  for a6 in range(256):
                    key = [a1, a2, a3, a4, a5, a6]
                    status = rdr.card_auth(rdr.auth_a, 10, key, uid)
                    if not status:
                      auth_key = key
                      break
        # Auth for block 10 (block 2 of sector 2) using default shipping key A
        print("authorised key: " + str(auth_key))
        if not rdr.card_auth(rdr.auth_a, 10, auth_key, uid):
          # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
          print("Reading block 10: " + str(rdr.read(10)))
          # Always stop crypto1 when done working
          rdr.stop_crypto()
          time.sleep(1)

# Calls GPIO cleanup
rdr.cleanup()
