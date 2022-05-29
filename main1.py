
from fo import FileOnline

# to send
fo = FileOnline("192.168.219.105", 8080)
fo.send("test.txt") # send file data to user
fo.close() # disconnect with user
