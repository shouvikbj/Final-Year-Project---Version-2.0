import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS comment(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER,
            username VARCHAR2(1000),
            cmnt VARCHAR2(10000000000000000000000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS commentBackUp AS SELECT * FROM comment WHERE 1=1;
    """)

def addComment(pid,username,cmnt):
    db.execute("INSERT INTO comment VALUES (NULL,?,?,?)",(pid,username,cmnt))
    db.execute("INSERT INTO commentBackUp VALUES (NULL,?,?,?)",(pid,username,cmnt))
    con.commit()

def getComments(pid):
    db.execute("SELECT cm.id,cm.pid,cm.username,cm.cmnt,u.firstname,u.lastname,u.image FROM users AS u INNER JOIN (SELECT c.id,c.pid,c.username,c.cmnt FROM comment AS c INNER JOIN post AS p ON (c.pid = p.id)) AS cm ON (cm.username = u.username) WHERE cm.pid=(?)",(pid,))
    comments = db.fetchall()
    return comments









#createTable()