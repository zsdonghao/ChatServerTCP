import socket

HOST = '52.11.137.117'    # The remote host
PORT = 5005              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

s.sendall(b'Hello, world')
data = s.recv(1024)
print(1,data)
data = s.recv(1024)
print(2,data)

for i in range(1000):
	s.send(('signin test%d 55555 0\r\n' % i).encode())
	data = s.recv(1024)
	print(i, data)
	
s.close()
#print('Received', repr(data))
