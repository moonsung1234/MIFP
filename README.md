
# MIFP (Moonsung International File Protocal)

파일을 주고받는데 쓰이는 프로토콜(protocal) 입니다.

<br/>

# Explain

파일을 소켓을 통해 공유할 수 있는 모듈이다.

<br/>

```python
# sender code

from fo import FileOnline

# to send
fo = FileOnline("192.168.219.105", 8080) # (my ip, my port)
fo.send("test.txt") # send file data to user
fo.close() # disconnect with user

```

<br/>

```python
# getter code

from fo import FileOnline

# to receive
fo = FileOnline("192.168.219.105", 8080) # (owner ip, owner port)
fo.receive() # receive file data to owner
fo.close() # disconnect with owner

```

<br/>

# More

- 텍스트(txt) 파일과 코드(py, js, c, cpp...) 파일만 전송되는것을 확인했으며, 이미지 파일의 전송기능도 내장되어 있긴 하지만 테스트 해보지는 않았다.

<br/>