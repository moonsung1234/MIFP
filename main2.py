
from fo import FileOnline

# to receive
fo = FileOnline("192.168.219.105", 8080)
fo.receive() # receive file data to owner
fo.close() # disconnect with owner

