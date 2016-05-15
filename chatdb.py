'''
Live Chat DB Class / logic method / respond method(TCP, HTTP)
'''

__author__ = 'hd311'
__date__ = '28 April 2015'


from mongoengine import * # dependency: pymongo==2.8 pillow
import hashlib  # python3 don't have md5 module, insteaded by hashlib
import datetime

''' -------------------------Connecting DB------------------------------ '''
print('Connecting to Mongodb...')
connect('chat-db', host='192.168.0.17', port=27017)
print('Connect Mongodb success')

''' -------------------------Defining DB-------------------------------- '''
class Friend(EmbeddedDocument):
    friend_id = StringField(max_length=30, required=True)
    accept = BooleanField(default=False)
    isinviter = BooleanField() # I am [inviter:1 invitee:0]

class Message(EmbeddedDocument):
    sender_id = StringField(min_length=5, max_length=30, required=True)
    message = StringField()
    create_date = DateTimeField(required=True, default=datetime.datetime.utcnow)

class User(Document):
    userid = StringField(min_length=5, max_length=30, required=True, unique=True) # if primary_key=True then pk=id=userid
    username = StringField(min_length=5, max_length=50)
    password = StringField(min_length=5, max_length=100, required=True)
    email = EmailField()
    gender = BooleanField(default=False, required=True) # [male:0 female:1] or using choices=('F','M')?
    age = IntField(min_value=0, max_value=150, default=10)
    portrait = ImageField(size=(500, 500, True)) # max size to store, can auto resized
    regist_date = DateTimeField(default=datetime.datetime.utcnow)
    multidevice = IntField(default=0) # num of devices login one userid
    friends_list = ListField(EmbeddedDocumentField(Friend))
    unread_msg = ListField(EmbeddedDocumentField(Message))

class Group(Document):
    owner = ReferenceField(User, reverse_delete_rule=CASCADE)
    members_list = ListField(ReferenceField(User)) 


''' ------------------------------------------------------------------ '''
class TCPresponse:
    '''
    Use TCP socket to respond client
    '''
    def respondUnlogin(self):
        self.sock.send('Please log-in before this process\r\n'.encode())
        print('Please log-in before this process')
    def respondPlslogout(self):
        self.sock.send('Please log-out before this process\r\n'.encode())
        print('Please log-out before this process')
    def respondFormatIncorrect(self):
        self.sock.send('Input format incorrect\r\n'.encode())
        print('Input format incorrect')
    def respondNoUserid(self):
        self.sock.send('No this user-id exist\r\n'.encode())
        print('No this user-id exist')
    def respondLoginSuccess(self):
        self.sock.send('Log-in success\r\n'.encode())
        print('Log-in success') 
    def respondPswIncorrect(self):
        self.sock.send('Password incorrect\r\n'.encode())
        print('Password incorrect')
    def respondLogoutSuccess(self):
        self.sock.send('Logout success\r\n'.encode())
        print('Logout success')
    def respondFormatIncorrect_gender(self):
        self.sock.send('Incorrect gender, pls input 0 for male, 1 for female\r\n'.encode())
        print('Incorrect gender, pls input 0 for male, 1 for female')
    def respondFormatIncorrect_age(self):             
        self.sock.send('Pls input an age between 0-150\r\n'.encode())
        print('Pls input an age between 0-150')
    def respondFormatIncorrect_userid(self):
        self.sock.send('The length of ID should be 5 to 30 characters\r\n'.encode())
        print('The length of ID should be 5 to 30 characters')
    def respondFormatIncorrect_userid(self):
        self.sock.send('The length of userid should be 5 to 30 characters\r\n'.encode())
        print('The length of userid should be 5 to 30 characters')
    def respondFormatIncorrect_password(self):
        self.sock.send('The length of  password should be 5 to 30 characters\r\n'.encode())
        print('The length of password should be 5 to 30 characters')  

    ''' '''
    def respondUserInfo(self, userid, username, email, gender, age, portrait, regist_date, friends_list=None):
        self.sock.send(('userid    | %s\r\n' % userid).encode())
        self.sock.send(('username  | %s\r\n' % username).encode())
        self.sock.send(('email     | %s\r\n' % email).encode())
        print('userid    | %s' % userid)
        print('username  | %s' % username)
        print('email     | %s' % email)
        if gender == False:
            self.sock.send('gender    | male\r\n'.encode())
            print('gender    | male')
        else:
            self.sock.send('gender    | female\r\n'.encode())
            print('gender    | female')
        self.sock.send(('age       | %s\r\n' % age).encode())
        self.sock.send('portrait  | can\'t display\r\n'.encode())
        self.sock.send(('register date | %s\r\n' % regist_date).encode())
        print('age       | %s' % age)
        print('portrait  | can\'t display')
        print('register date | %s' % regist_date)

        if friends_list==None:
            return
        self.sock.send('Friend list\r\n'.encode())
        print('Friend list')
        for f in friends_list:        
            self.sock.send(('%s accept:%s I-am-inviter:%s\r\n' % (f.friend_id, f.accept, f.isinviter)).encode())
            print('%s accept:%s I-am-inviter:%s' % (f.friend_id, f.accept, f.isinviter))
    def respondNotFriendYet(self):
        self.sock.send('This id is not your friend, or he/she did not accept you yet\r\n'.encode())
        print('This id is not your friend, or he/she did not accept you yet')
    def respondUnreadMsg(self, unread_msg):
        self.sock.send('Unread message list:\r\n'.encode())
        print('Unread message list:')
        for msg in unread_msg:        
            self.sock.send(('sender_id: %s message: %s create_date: %s\r\n' % (msg.sender_id, msg.message, msg.create_date)).encode())
            print('sender_id: %s message: %s create_date: %s' % (msg.sender_id, msg.message, msg.create_date))
    def respondCannotAddYourself(self):
        self.sock.send('You can\'t add yourself\r\n'.encode())
        print('You can\'t add yourself')
    def respondAlreadyInFriendList(self):
        self.sock.send('Already in friends_list. or Waiting you or he/she to accepted\r\n'.encode())
        print('Already in friends_list. or Waiting you or he/she to accepted')
    def respondInviteSendSuccess(self):
        self.sock.send('Send invitation done\r\n'.encode())
        print('Send invitation done')
    def respondDelFriendSuccess(self):
        self.sock.send('Delete success\r\n'.encode())
        print('Delete success')
    def respondAcceptInviteSuccess(self):
        self.sock.send('Accept invitation success\r\n'.encode())
        print('Accept invitation success')    
    def respondCannotAccept(self):
        self.sock.send('No invition from this id or this id is your friend already\r\n'.encode())
        print('No invition from this id or this id is your friend already')      
    def respondExistUserid(self):
        self.sock.send('Existing this userid\r\n'.encode())
        print('Existing this userid')
    def respondRegistSuccess(self):
        self.sock.send('Sign-in success\r\n'.encode())
        print('Sign-in success')
    def respondTrySendMsg(self):
        self.sock.send('Server got the message and Trying to send\r\n'.encode())
        print('Server got the message and Trying to send')
    def respondUnknownCommand(self):
        self.sock.send('Unknown command(\'help\' for more info)\r\n'.encode())
        print('Unknown command (\'help\' for more info)')
    def respondHelp(self):
        self.sock.send('               [cmd]     [others]\r\n'.encode())
        self.sock.send('Sign In      | signin    userid      password    gender\r\n'.encode())
        self.sock.send('             |           [5-30 char] [5-20 char] [male:0 female:1]\r\n'.encode())
        self.sock.send('Log  In      | login     userid password\r\n'.encode())
        self.sock.send('Add Friend   | addfriend friend_id\r\n'.encode())
        self.sock.send('Accept Friend| acceptfriend friend_id\r\n'.encode())
        self.sock.send('Delete Friend| delfriend friend_id\r\n'.encode())
        self.sock.send('Change info  | changeinfo   key context\r\n'.encode())
        self.sock.send('             |   key <username, password, email, gender, age, portrait>\r\n'.encode())
        self.sock.send('             |   example <changeinfo gender 1> change gender to female\r\n'.encode())
        self.sock.send('Check info   | checkinfo\r\n'.encode())
        self.sock.send('Check unread | checkunread\r\n'.encode())
        self.sock.send('Check friend | checkfriendinfo friend_id\r\n'.encode())
        self.sock.send('Send msg     | sendmsg   friend_id msg\r\n'.encode())
        self.sock.send('Log out      | logout\r\n'.encode())
        print('               [cmd]     [others]')
        print('Sign In      | signin    userid      password    gender')
        print('             |           [5-30 char] [5-20 char] [male:0 female:1]')
        print('Log  In      | login     userid password')
        print('Add Friend   | addfriend friend_id')
        print('Accept Friend| acceptfriend friend_id')
        print('Delete Friend| delfriend friend_id')
        print('Change info  | changeinfo   key context')
        print('             |   key <username, password, email, gender, age, portrait>')
        print('             |   example <changeinfo gender 1> change gender to female')
        print('Check info   | checkinfo')
        print('Check unread | checkunread')
        print('Check friend | checkfriendinfo friend_id')
        print('Send msg     | sendmsg   friend_id msg')
        print('Log out      | logout')

''' ----------------------------------------------------------- '''
def pswmd5(psw):
    return hashlib.sha224(psw.encode()).hexdigest() # str
''' ----------------------------------------------------------- '''

class dhchat(TCPresponse):
    '''
    Achieve all chat logic:
    chat     -----  classify request type, then use the following logic methods 
    signin          signin haodong 55555 0  [userid, password, gender(0=male, 1=female)]  register a new user
    login           login haodong 55555     [userid, password]  log in an account
    logout          logout                  []                  log out from current account
    addfriend       addfriend haodong       [friend_id]         send invition to a friend by friend's id
    acceptfriend    acceptfriend haodong    [friend_id]         when a friend want to add you, you can accept he/she by his/her id
    delfriend       delfriend haodong       [friend_id]         delete a friend
    changeinfo      changeinfo email dhsig552@163.com [info_type, info_content] change current account's information
    checkinfo       checkinfo               []                  check current account's information
    checkunread     checkunread             []                  check current account's unread message, after check, all unread message will be deleted from database(can only check once)
    checkfriendinfo checkfriendinfo haodong [friend_id]         check your friend's information by friend's id
    sendmsg         sendmsg haodong hello   [friend_id, message]send a message to a friend
    '''
    def __init__(self, addr, sock):
        TCPresponse.__init__(self)
        self.myid = '_unlogin'
        self.addr = addr
        self.ip = addr[0]
        self.port = addr[1]
        self.sock = sock
        self.multidevice = 0 # num of devices login one userid
        
    def __login(self, msg):
        if self.myid != '_unlogin': # check status
            self.respondUnlogin()
            return
        msg = msg.split()
        if len(msg) != 2:
            self.respondFormatIncorrect()
            return
        userid = msg[0]
        password = msg[1]
        passwordMD5 = pswmd5(password)

        me = User.objects(userid=userid).first()
        # check user if exist in db
        if me == None:
            self.respondNoUserid()
            return
        # check password in db
        if me.userid == userid and me.password == passwordMD5:
            self.myid = userid
            self.multidevice += 1
            self.respondLoginSuccess()
            return (2, self.myid) # (2, 'haodong')
        else:
            self.respondPswIncorrect()
            return

    def __logout(self): # __logout(self)
        r_temp = self.myid
        self.myid = '_unlogin'
        self.multidevice -= 1
        self.respondLogoutSuccess()
        return (3, r_temp) # (3, 'haodong')

    def __changeinfo(self, msg):
        if self.myid == '_unlogin': # check status
            self.respondUnlogin()
            return
        msg = msg.split(' ',1)
        key = msg[0]
        context = msg[1]
        y = User.objects(userid=self.myid).first()

        if key == 'username':
            y.username = context
        elif key == 'password':
            y.password = context 
        elif key == 'email':
            if not ('@' in context ): # check email format
                self.respondFormatIncorrect()
                return
            y.email = context
        elif key == 'gender':
            if not (context == '0' or context == '1'):
                self.respondFormatIncorrect_gender()
                return
            y.gender = context
        elif key == 'age':
            context = int(context)
            if not (0 < context <= 150):
                self.respondFormatIncorrect_age()
                return
            y.age = context
        elif key == 'portrait':
            #self.sock.send('Don\'t support portrait at the moment\r\n'.encode())
            #print('Don\'t support portrait at the moment')
            pass
        else:
            self.respondFormatIncorrect()
        y.save() # save db
        self.__checkinfo()

    def __checkinfo(self): # __checkinfo(self)
        if self.myid == '_unlogin':
            self.respondUnlogin()
            return
        me = User.objects(userid=self.myid).first()
        self.respondUserInfo(userid=self.myid, username=me.username, email=me.email, gender=me.gender, age=me.age, portrait=me.portrait, regist_date=me.regist_date, friends_list=me.friends_list)

    def __checkfriendinfo(self, msg):
        friend_id = msg           
        if self.myid == '_unlogin':
            self.respondUnlogin()
            return
        if not User.objects(userid=self.myid, friends_list__match={"friend_id":friend_id,"accept":True}).first():
            self.respondNotFriendYet()
            return      
        f = User.objects(userid=friend_id).first()
        self.respondUserInfo(userid=friend_id, username=f.username, email=f.email, gender=f.gender, age=f.age, portrait=f.portrait, regist_date=f.regist_date)
    
    def __checkunread(self): # __checkunread(self)
        me = User.objects(userid=self.myid).only('unread_msg').first()
        self.respondUnreadMsg(unread_msg=me.unread_msg)
        #u = User.objects(userid=self.myid).only('unread_msg').first()      
        User.objects(userid=self.myid).update_one(pull_all__unread_msg=me.unread_msg) # remove all from list

    def __addfriend(self, msg):
        if self.myid == '_unlogin': # check status
            self.respondUnlogin()
            return
        friend_id = msg
        if not (5 <= len(friend_id) <= 30): # check id length
            self.respondFormatIncorrect_userid()
            return
        if self.myid == friend_id: 
            self.respondCannotAddYourself()
            return   
        # check id if not id exist in db
        if User.objects(userid=friend_id).first() == None:
            self.respondNoUserid()
            return
        # check if he/she in user's friends_list already
        if User.objects(userid=self.myid, friends_list__friend_id=friend_id): # Already in friends_list. or Waiting you or he/she to accepted
            self.respondAlreadyInFriendList()
            return
        
        f = Friend(friend_id=friend_id, accept=False, isinviter=True) # add friend to my document
        User.objects(userid=self.myid).update_one(push__friends_list=f)
        
        f2 = Friend(friend_id=self.myid, accept=False, isinviter=False) # add friend to friend's document
        User.objects(userid=friend_id).update_one(push__friends_list=f2)
        self.respondInviteSendSuccess()

    def __delfriend(self, msg):
        if self.myid == '_unlogin':  # check status
            self.respondUnlogin()
            return

        friend_id = msg
        # try to delete friend
        if User.objects(userid=self.myid, friends_list__match={"friend_id":friend_id,"accept":True}).first():
            User.objects(userid=self.myid, friends_list__friend_id=friend_id).update_one(set__friends_list__S__accept=False)
            User.objects(userid=friend_id, friends_list__friend_id=self.myid).update_one(set__friends_list__S__accept=False)
            self.respondDelFriendSuccess()
        else:
            self.respondNotFriendYet()
   
    def __acceptfriend(self, msg):
        if self.myid == '_unlogin':  # check status
            self.respondUnlogin()
            return
        inviter_id = msg
        # try accept friend
        if User.objects(userid=self.myid, friends_list__match={"friend_id":inviter_id,"accept":False,"isinviter":False}).first():
            User.objects(userid=self.myid, friends_list__friend_id=inviter_id).update_one(set__friends_list__S__accept=True)
            User.objects(userid=inviter_id, friends_list__friend_id=self.myid).update_one(set__friends_list__S__accept=True)
            self.respondAcceptInviteSuccess()
        else: 
            # No invition from this id or this id is your friend already
            self.respondCannotAccept()

    def __signin(self, msg):
        if self.myid != '_unlogin':  # check status
            self.respondPlslogout()
            return
        msg = msg.split()
        if len(msg) != 3 or not (msg[2] =='0' or msg[2] == '1'): 
            self.respondFormatIncorrect()
            return
        userid = msg[0]
        password = msg[1]
        passwordMD5 = pswmd5(password) # DH: fix length with 56 characters
 
        if int(msg[2]) == 0: # check gender
            gender = False
        else:
            gender = True
        if not(5 <= len(userid) <= 30): # check id length
            self.respondFormatIncorrect_userid()
            return
        elif not(5 <= len(password) <=30): # check psw length
            self.respondFormatIncorrect_password()     
            return
        # check user-id if exist in db
        if User.objects(userid=userid).first():
            self.respondExistUserid()   # exist this userid, can't use this id to regist
            return
        User(userid=userid, password=passwordMD5, gender=gender).save()
        self.respondRegistSuccess()
        
    def __sendmsg(self, msg):
        msg = msg.split(' ',1)
        if len(msg) != 2:
            self.respondFormatIncorrect()
            return
        friend_id = msg[0]
        message = msg[1]
        #import pprint # speed test
        #pprint.pprint(User.objects(userid=self.myid, friends_list__match={"friend_id":friend_id,"accept":True}).explain())
        #try SENDMSG to an online user, otherwise store msg to unread_msg
        if User.objects(userid=self.myid, friends_list__match={"friend_id":friend_id,"accept":True}).first(): 
            self.respondTrySendMsg()
            msgtofriend = self.myid + ' ' + message
            return (1, friend_id, msgtofriend) # (1, 'test1', 'haodong hi test1 I am haodong')
        else:
            self.respondNotFriendYet()

    def __help(self): # help()
        self.respondHelp()        

    #functions = dict(sendmsg=__sendmsg, sigin=__signin, addfriend=__addfriend,
    #        delfriend=__delfriend, acceptfriend=__acceptfriend, checkinfo=__checkinfo,
    #        checkunread=__checkunread, checkfriendinfo=__checkfriendinfo, changeinfo=__changeinfo,
    #        logout=__logout, login=__login, help=__help)

    def chat(self,command):
        command = command.strip().split(' ',1)
        cmd = command[0]
        try:
            msg = command[1]
        except:
            msg = ''

        #r = self.functions[cmd](msg=msg)
        '''
        try:
            r = functions[cmd](msg)
        except:
            r = None
            self.respondUnknownCommand()'''

        if cmd=="sendmsg":
            r = self.__sendmsg(msg)
        elif cmd=='signin':
            r = self.__signin(msg)
        elif cmd=='login':
            r = self.__login(msg)
        elif cmd=='addfriend':
            r = self.__addfriend(msg)
        elif cmd=='delfriend':
            r = self.__delfriend(msg)
        elif cmd=='acceptfriend':
            r = self.__acceptfriend(msg)
        elif cmd=='checkinfo':
            r = self.__checkinfo()
        elif cmd=='checkunread':
            r = self.__checkunread()
        elif cmd=='checkfriendinfo':
            r =self.__checkfriendinfo(msg)
        elif cmd=='changeinfo':
            r =self.__changeinfo(msg)
        elif cmd=='logout':
            r = self.__logout()
        elif cmd=='help':
            r = self.__help()
        else:
            r = None
            self.respondUnknownCommand()
        return r # pass info back

''' --------------------- '''
def unread_push(userid, message): # Add an unread msg to user document, if user is offline
    msg = message.split(' ',1)
    sender_id = msg[0]
    message = msg[1]
    u = Message(sender_id=sender_id,message=message)
    User.objects(userid=userid).update_one(push__unread_msg=u)


''' -------------------Simulation--------------------------------- '''
if __name__=="__main__":
    print("Live Chat User System Simulation (\'help\' for more info)")
    '''
    i = dhchat()
    while True:
        command = []
        while not command:
            command = input(' > ')
        i.chat(command)
    '''





