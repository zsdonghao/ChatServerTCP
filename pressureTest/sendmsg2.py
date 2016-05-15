import socket

HOST = '52.11.137.117'    # The remote host
#HOST = ''	# local host
PORT = 5005              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = s.recv(1024)
print(1,data)
data = s.recv(1024)
print(2,data)

import time
#time.sleep(1)

s.send('login test2 55555\r\n'.encode())
data = s.recv(1024)
print(3,data)

tStart = time.time()
numOfMsg = 100
for i in range(numOfMsg):
	#s.send('sendmsg test1 hello\r\n'.encode())
	s.send('sendmsg test10 hello\r\n'.encode())
	data = s.recv(1024)
	print(i, data)
tEnd = time.time()
print('Time: ', tEnd-tStart)
print('Average Time: ', (tEnd-tStart)/numOfMsg)
	
s.close()