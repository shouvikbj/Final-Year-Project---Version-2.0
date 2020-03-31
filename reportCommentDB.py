import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS reportComment(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER,
            username VARCHAR2(1000),
            cmnt VARCHAR2(10000000000000000000000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS reportCommentBackUp AS SELECT * FROM reportComment WHERE 1=1;
    """)

def addReportComment(pid,username,cmnt):
    db.execute("INSERT INTO reportComment VALUES (NULL,?,?,?)",(pid,username,cmnt))
    db.execute("INSERT INTO reportCommentBackUp VALUES (NULL,?,?,?)",(pid,username,cmnt))
    con.commit()

def getReportComments(pid):
    db.execute("SELECT * FROM reportComment WHERE pid=(?)",(pid,))
    comments = db.fetchall()
    return comments


def deleteAllComment(pid):
    db.execute("DELETE FROM blogComment WHERE pid=(?)",(pid,))
    con.commit()





createTable()