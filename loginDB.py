import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username VARCHAR2(50) PRIMARY KEY,
            firstname VARCHAR2(50) NOT NULL,
            lastname VARCHAR2(50) NOT NULL,
            email VARCHAR2(50) NOT NULL,
            phone VARCHAR2(13) NOT NULL,
            password VARCHAR2(100) NOT NULL,
            image VARCHAR2(150) DEFAULT 'defaultProfileImage.png'
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS usersBackUp AS SELECT * FROM users  WHERE 1=1;
    """)

def createUser(username,firstname,lastname,email,phone,password,image):
    db.execute("INSERT INTO users VALUES(?,?,?,?,?,?,?)",(username,firstname,lastname,email,phone,password,image))
    db.execute("INSERT INTO usersBackUp VALUES(?,?,?,?,?,?,?)",(username,firstname,lastname,email,phone,password,image))
    con.commit()

def login(username):
    db.execute("SELECT username,password FROM users WHERE username = (?)",(username,))
    details = db.fetchall()
    return details

def getUser(username):
    db.execute("SELECT * FROM users WHERE username = (?)",(username,))
    user = db.fetchall()
    return user

def updateProfilePic(username,filename):
    db.execute("UPDATE users SET image = (?) WHERE username = (?)",(filename,username))
    db.execute("UPDATE usersBackUp SET image = (?) WHERE username = (?)",(filename,username))
    con.commit()

def listProfilePics():
    db.execute("SELECT image FROM users")
    profilePics = db.fetchall()
    return profilePics

def getPassword(username):
    db.execute("SELECT phone,password,username,email FROM users WHERE username = (?)",(username,))
    password = db.fetchall()
    return password

def updateDetails(username,firstname,lastname,phone,password):
    db.execute("UPDATE users SET firstname=(?),lastname=(?),phone=(?),password=(?) WHERE username=(?)",(firstname,lastname,phone,password,username))
    db.execute("UPDATE usersBackUp SET firstname=(?),lastname=(?),phone=(?),password=(?) WHERE username=(?)",(firstname,lastname,phone,password,username))
    con.commit()

def getUsers(searchbox):
    db.execute("SELECT username,firstname,lastname,image FROM users WHERE firstname LIKE '%{}%' or lastname LIKE '{}%' order by firstname".format(searchbox,searchbox))
    userList = db.fetchall()
    return userList

def getAllUsers():
    db.execute("SELECT username,firstname,lastname,image FROM users ORDER BY firstname")
    allUsers = db.fetchall()
    return allUsers

def getAll():
    db.execute("SELECT * FROM users")
    users = db.fetchall()
    return users

def deleteUser(username):
    db.execute("DELETE FROM users WHERE username=(?)",(username,))
    con.commit()

def getUserForChat(username):
    db.execute("SELECT username, firstname, lastname, phone, image FROM users WHERE username=(?)", (username,))
    user = db.fetchall()
    return user

def getName(username):
    db.execute("SELECT firstname,lastname,image FROM users WHERE username=(?)",(username,))
    user_name = db.fetchall()
    return user_name

#createTable()
#createUser("abc","shouvik","bajpayee","sBajpayee@GangPayee.com","9734282057","abc12345")


