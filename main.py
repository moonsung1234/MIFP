
from .fo import FileOnline


# to send
fo = FileOnline("my host", "my port")
fo.send("test.txt") # send file data to user
fo.close() # disconnect with user


# to receive
fo = FileOnline("owner host", "owner port")
fo.receive("test.txt") # receive file data to owner
fo.close() # disconnect with owner