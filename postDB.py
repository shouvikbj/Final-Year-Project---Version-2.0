import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS post(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR2(1000),
            desc VARCHAR2(1000000000000000000),
            media VARCHAR2(1000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS postBackUp AS SELECT * FROM post WHERE 1=1;
    """)

def createPost(username,desc,media):
    db.execute("INSERT INTO post VALUES (NULL,?,?,?)",(username,desc,media))
    db.execute("INSERT INTO postBackUp VALUES (NULL,?,?,?)",(username,desc,media))
    con.commit()

def getAllPost():
    db.execute("""
        SELECT u.image,u.firstname,u.lastname,p.username,p.desc,p.media,p.id FROM users AS u INNER JOIN post AS p ON (p.username=u.username)
    """)
    post = db.fetchall()
    return post

def getPost(pid):
    db.execute("""
        SELECT u.image,u.firstname,u.lastname,p.username,p.desc,p.media,p.id FROM users AS u INNER JOIN post AS p ON (p.username=u.username) WHERE p.id={}
    """.format(pid))
    post = db.fetchall()
    return post

def getUserPost(username):
    db.execute("""
        SELECT u.image,u.firstname,u.lastname,p.username,p.desc,p.media,p.id FROM users AS u INNER JOIN post AS p ON (p.username=u.username) WHERE u.username=(?)
    """,(username,))
    userPost = db.fetchall()
    return userPost

def deletePost(pid):
    db.execute("DELETE FROM post WHERE id=(?)",(pid,))
    con.commit()

#createTable()