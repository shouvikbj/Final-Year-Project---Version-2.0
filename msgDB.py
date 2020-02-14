import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS msgs(
            username VARCHAR2(50) NOT NULL,
            msg VARCHAR2(10000000000000000000000000000000000) NOT NULL
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS msgsBackUp AS SELECT * FROM msgs WHERE 1=1;
    """)

def msgEntry(username,msg):
    db.execute("INSERT INTO msgs VALUES (?,?)",(username,msg))
    db.execute("INSERT INTO msgsBackUp VALUES (?,?)",(username,msg))
    con.commit()

def getMsgs():
    db.execute("SELECT m.username,u.firstname,u.lastname,u.image,m.msg FROM msgs AS m INNER JOIN users AS u ON (m.username=u.username)")
    msgs = db.fetchall()
    return msgs







#createTable()