#!/usr/bin/python

#do not print things yet!
import cgi,cgitb,hashlib,Cookie
cgitb.enable()
form = cgi.FieldStorage()

# set some constants so we can replace numbers up here
USER_EXPIRE_TIME =     60 * 60 # 1 hour
PASSWORD_EXPIRE_TIME = 60 * 60  # 1 minutes

# create the cookie with a dummy value
c=Cookie.SimpleCookie()
c['loaded']='True'

#set up your page in pieces, do not print in your code, just
#append to the body if you want to see text.
head = '''
<html>
<head><title>Login page</title>
<style>
.login-page {
  width: 450px;
  padding: 8% 0 0;
  margin: auto;
}
.form {
  position: relative;
  z-index: 1;
  background: #FFFFFF;
  max-width: 450px;
  margin: 0 auto 100px;
  padding: 45px;
  text-align: center;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
}
.form input {
  font-family: "Roboto", sans-serif;
  outline: 0;
  background: #f2f2f2;
  width: 100%;
  border: 0;
  margin: 0 0 15px;
  padding: 15px;
  box-sizing: border-box;
  font-size: 14px;
}
.form input[type=submit] {
  font-family: "Roboto", sans-serif;
  text-transform: uppercase;
  outline: 0;
  background: #BA7A9F;
  width: 100%;
  border: 0;
  padding: 15px;
  color: #FFFFFF;
  font-size: 14px;
  -webkit-transition: all 0.3 ease;
  transition: all 0.3 ease;
  cursor: pointer;
}
.form submit:hover,.form submit:active,.submit button:focus {
  background: #BA7A9F;
}
.form .message {
  margin: 15px 0 0;
  color: #b3b3b3;
  font-size: 12px;
}

.form .message a {
  color: #4CAF50;
  text-decoration: none;
}
.form .register-form {
  display: none;
}
.container {
  position: relative;
  z-index: 1;
  max-width: 400px;
  margin: 0 auto;
}
.container:before, .container:after {
  content: "";
  display: block;
  clear: both;
}
.container .info {
  margin: 10px auto;
  text-align: center;
}
.container .info h1 {
  margin: 0 0 1px;
  padding: 0;
  font-size: 36px;
  font-weight: 300;
  color: #1a1a1a;
}
.container .info span {
  color: #4d4d4d;
  font-size: 12px;
}
.container .info span a {
  color: #000000;
  text-decoration: none;
}
.container .info span .fa {
  color: #EF3B3A;
}
body {
  background: #AFD5EA;; /* fallback for old browsers */
  background: -webkit-linear-gradient(right, #AFD5EA;, #8DC26F);
  background: -moz-linear-gradient(right, #AFD5EA;, #8DC26F);
  background: -o-linear-gradient(right, #AFD5EA;, #8DC26F);
  background: linear-gradient(to left, #AFD5EA;, #8DC26F);
  font-family: "Roboto", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;      
}
</style>
</head>
<body>
   '''
body = ""
foot = '''
</body>
</html>
'''





def authenticate(u,p):
    users = open('../data/users.txt','r').read().split('\n')
    #don't worry about this
    users = [each.split(',') for each in users]
    ##debug by adding info to the body
    #body += str(users)
    users.remove( [""])
    hashed = hashlib.sha256(p).hexdigest()
    for a in users:
        if a[0] == username:
            return a[1]==hashed
    return False



#writeOrReplace writes a logged in user to a text file
#this should only be called after a user authenticates
def writeOrReplace(filename,username,number,IP):
    #check if you need to remove old values
    f = open(filename,'r').read().split("\n");
    data = [each.split(',') for each in f]
    write = False
    for i in range(len(data))[::-1]:
        if data[i]==['']:
            write = True
            data.pop(i)
        elif data[i][0]==username:
            data.pop(i)
            write = True
    ##remove a line if needed
    if write:
        res = ""
        for each in data:
            res+= ",".join(each)+"\n"
        f = open(filename,'w')
        f.write(res)
        f.close()
    #append the line to the file
    f = open(filename,'a')
    f.write(username+","+str(number)+","+str(IP)+"\n")
    f.close()
    
def createCookie(c,username,ID):
    c['username']=username
    c['ID']=ID
    c['username']['expires']=USER_EXPIRE_TIME
    c['ID']['expires']=PASSWORD_EXPIRE_TIME

    
if 'username' in form and 'password' in form:
    username = form.getvalue('username')
    password = form.getvalue('password')
    if authenticate(username,password):
        import os,random
        IP = os.environ['REMOTE_ADDR']
        ID = random.randint(1000000,9999000)
        
        #print some debug info at the top of the page:
        #body += "Success!<br>"
        #body += "Random Number: "+str(ID)+"<br>"
        #body += "IP: "+ IP + "<br>"

        #write to a file
        writeOrReplace('../data/loggedin.txt',username,ID,IP)

        #create a cookie:
        createCookie(c,username,ID)
        ##debug statements
        #body+= "cookie created<br>"
        #for each in c:
        #    body+= each+":"+c[each].value+"<br>"

        #attach a link:
        body+='<a href="mainpage.py">Go To Main Page</a><br>'
    else:
        body += 'Failed to authenticate.<a href="login.py">Try Again</a>'
else:
    body = '''
<div class="login-page">
  <div class="form">
    <form class=login-form>
    <p>Don't have an account: <a href="createaccount.py">Create account here</a></p>
    <h1>Log in:</h1><br>
      username <input type="text" name="username" placeholder="username">
      password <input type="password" name="password" placeholder="password">
      <input type="submit" value="log in">
    </form>
    <a href="../../finalproject.html">Back to Penne for Your Thoughts Home</a>
  </div>
</div>
'''                    
#    <h1>Log in:</h1>
##    <form action="login.py">
##    Username: <input type="text" name="username"><br>
##    Password: <input type="password" name="password"><br>
##    <input type="submit" value="log in">
##    '''

#print the cookie first, then content type, then the page
print c
print 'content-type: text/html\n'
print head
print body
print foot


