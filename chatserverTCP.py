'''
Original Program from 《python基础教程 第二版》24-5
Modify for real chatserver

Func:   
    1. Add friend and send message to friend
Disadv:
    1. Did not consider multiple devices login one account
    2. No groud chat

'''
__author__ = 'hd311'
__date__ = '28 April 2015'


from asyncore import dispatcher
from asynchat import async_chat
import socket, asyncore
import chatdb  # DH add: define db and logic method


PORT = 5005
NAME = 'ChatServer'


class ChatSession(async_chat):
    """
    Handle connection between server and one client
    N clients mean N chatsession instances
    """         
    onlineid = {}   # DH add: static variables(share will all instances)
                    # dict {'_unlogin', ('192.168.21.17', 5005)} # store login userid and its addr
                    #  server->ChatServer  sock->conn  addr->addr
    def __init__(self, server, sock, addr):  # DH add addr
        # Standard setting
        async_chat.__init__(self, sock)
        self.server = server
        self.addr = addr             # DH add
        self.set_terminator(b'\r\n') # Py3
        self.data = []
        self.dhchat = chatdb.dhchat(addr,sock) # DH add
        self.push(('Welcome to %s\r\n' % self.server.name).encode()) # py3
        sock.send('ChatSession started (\'help\' for more info)\r\n'.encode()) # DH add
        self.myid = '_unlogin'
        self.temp = ''

    def collect_incoming_data(self, data):
        self.data.append(data.decode())# Py3 娃can't decode 'utf-8','replace'
        #self.data.append(str(data))# error
        #print('collect_incoming_data ', data.decode()) # DH add

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        #self.server.broadcast(line)
        print('Data from', self.addr, '>', line)  # DH add addr
        #print(self.chat.ip)
        dh = self.dhchat.chat(line) # DH add: chat logic service
        #print('RETURN',type(dh),dh)
        if dh == None:
            pass
        elif dh[0] == 1:    # if return 1 means: try SENDMSG to an online user, otherwise store msg to unread_msg
            try:            #>> (1, 'test1', 'haodong hi test1 I am haodong')
                addr = self.onlineid[dh[1]]
                self.server.sendmsg(addr=addr,line=dh[2])
            except:         # when userid(friend_id) is offline
                chatdb.unread_push(userid=dh[1], message=dh[2])
                print('This user is offline, save msg to unread_msg')
        elif dh[0] == 2:   # if return 2 means: LOGIN #>> (2, 'haodong')
            '''try:
                self.onlineid[dh[1]]
            except KeyError: 	# means this id didn't login on other device, than login on this device
                self.onlineid[dh[1]] = self.addr
                self.myid = dh[1]'''
            self.onlineid[dh[1]] = self.addr
            print('All onlineid ', self.onlineid)
            self.temp = dh[1]
            #print('login', dh[1], self.addr)
        elif dh[0] == 3:   # if return 3 means: LOGOUT  #>> (3, 'haodong')
            del self.onlineid[dh[1]]
            #print('logout ', self.myid, dh[1])  
            self.myid = '_unlogin'
            print('All onlineid ', self.onlineid)

    def handle_close(self):
        try:
            del self.onlineid[self.temp]
            self.myid = '_unlogin'
        except:
            print('Did not login when disconnect')
        print('All onlineid ', self.onlineid) # show all online id
        async_chat.handle_close(self)
        self.server.disconnect(self)

class ChatServer(dispatcher):
    """
    Accept connection and instantiate a new chatsession for each client
    """
    def __init__(self, port, name):
        # Standard setup tasks
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        self.sessions = []
        
    def disconnect(self, session):
        print('Disconnect', session.addr) # DH add
        self.sessions.remove(session)

    def broadcast(self, line): 
        for session in self.sessions:
            line = line + '\r\n'
            session.push(line.encode())  # py3 
            #print(session.addr) # DH add: print all clients' (ip, port)

    def sendmsg(self, addr, line):  # DH add: if user online, send msg to the user, otherwise store msg in db
        line = line + '\r\n'
        for session in self.sessions:
            if addr == session.addr:
                session.push(line.encode())

    def handle_accept(self):
        conn, addr = self.accept()
        print('Connect from', addr) # DH add
        conn.send('Thank you for connect\r\n'.encode())
        self.sessions.append(ChatSession(server=self, sock=conn, addr=addr)) # DH add addr

if __name__ == '__main__':
    print('Start ChatServer')
    s = ChatServer(PORT, NAME)
    try: asyncore.loop()
    except KeyboardInterrupt: print('Stop ChatServer')













