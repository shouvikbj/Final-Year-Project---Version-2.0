import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS messanger(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender VARCHAR2(100) NOT NULL,
            receiver VARCHAR2(100) NOT NULL,
            msg VARCHAR2(10000000000000000000000000000000000) NOT NULL
        )
    """)
    db.execute("""
        CREATE TABLE IF NOT EXISTS messangerBackUp AS SELECT * FROM messanger WHERE 1=1;
    """)

def putMsg(sender,receiver,msg):
    db.execute("INSERT INTO messanger values (NULL,?,?,?)",(sender,receiver,msg))
    db.execute("INSERT INTO messangerBackUp values (NULL,?,?,?)",(sender,receiver,msg))
    con.commit()

def getMsg(sender,receiver):
    db.execute("SELECT * FROM messanger WHERE ((sender=(?) AND receiver=(?)) OR (receiver=(?) AND sender=(?)))",(sender,receiver,sender,receiver))
    chats = db.fetchall()
    return chats




#createTable()