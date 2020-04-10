import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS moments(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR2(1000),
            text VARCHAR2(100000000000),
            image VARCHAR2(100000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS momentsBackUp AS SELECT * FROM moments WHERE 1=1;
    """)


def addMoment(username,text,image):
    db.execute("INSERT INTO moments VALUES (NULL,?,?,?)",(username,text,image))
    db.execute("INSERT INTO momentsBackUp VALUES (NULL,?,?,?)",(username,text,image))
    con.commit()

def getMoments(username):
    db.execute("SELECT text,image FROM moments WHERE username=(?)",(username,))
    moments = db.fetchall()
    return moments

def getMomentsForAccount(username):
    db.execute("SELECT image FROM moments WHERE username=(?)",(username,))
    moments = db.fetchall()
    return moments


#createTable()
#def drop():
#    db.execute("DROP TABLE moments")
#    db.execute("DROP TABLE momentsBackUp")
#    con.commit()
#
#drop()

