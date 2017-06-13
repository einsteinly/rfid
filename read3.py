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
        # Auth for block 10 (block 2 of sector 2) using default shipping key A
	status = rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid)
	print(status)
        if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
          # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
          print("Reading block 10: " + str(rdr.read(10)))
          # Always stop crypto1 when done working
          rdr.stop_crypto()
	  time.sleep(1)

# Calls GPIO cleanup
rdr.cleanup()
