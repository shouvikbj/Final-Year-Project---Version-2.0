import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS share(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR2(1000),
            user_name VARCHAR2(10000000),
            user_image VARCHAR2(10000000),
            postid INTEGER,
            text VARCHAR2(1000000000000000000),
            name VARCHAR2(100000),
            image VARCHAR2(100000),
            desc VARCHAR2(100000000000000000000000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS shareBackUp AS SELECT * FROM share WHERE 1=1;
    """)

def createSharedPost(username,user_name,user_image,postid,text,name,image,desc):
    db.execute("INSERT INTO share VALUES (NULL,?,?,?,?,?,?,?,?)",(username,user_name,user_image,postid,text,name,image,desc))
    db.execute("INSERT INTO shareBackUp VALUES (NULL,?,?,?,?,?,?,?,?)",(username,user_name,user_image,postid,text,name,image,desc))
    con.commit()

def getSharedPost():
    db.execute("SELECT * FROM share")
    sharedPosts = db.fetchall()
    return sharedPosts

def getSharedPosts(username):
    db.execute("SELECT * FROM share WHERE username=(?)",(username,))
    sharedPosts = db.fetchall()
    return sharedPosts

def deleteSharedPost(pid):
    db.execute("DELETE FROM share WHERE id=(?)",(pid,))
    con.commit()


#createTable()

