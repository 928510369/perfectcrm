from django.test import TestCase

# Create your tests here.
import socket
# socket_server=socket.socket()
# socket_server.bind(("localhost",8000))
# socket_server.listen(5)
# arg,addr=socket_server.accept()
# arg.recv(1024)
# arg.send("hello")

class A(object):
    def __init__(self):
        self.name="a"
        print("A")
class B(A):
    def __init__(self):
        super(B,self).__init__()
        print(self)
        print("B")
b=B()
print(b.name)