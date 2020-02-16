import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS map(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR2(1000),
            lat VARCHAR2(100),
            lng VARCHAR2(100),
            category VARCHAR2(500),
            desc VARCHAR2(100000000000000000000000),
            media VARCHAR2(1000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS mapBackUp AS SELECT * FROM map WHERE 1=1;
    """)

def createPost(username,lat,lng,category,desc,media):
    db.execute("INSERT INTO map VALUES (NULL,?,?,?,?,?,?)",(username,lat,lng,category,desc,media))
    db.execute("INSERT INTO mapBackUp VALUES (NULL,?,?,?,?,?,?)",(username,lat,lng,category,desc,media))
    con.commit()

def getAllPosts():
    db.execute("SELECT id,lat,lng,category FROM map")
    posts = db.fetchall()
    return posts

def getPost(pid):
    db.execute("""
        SELECT u.image,u.firstname,u.lastname,m.id,m.username,m.lat,m.lng,m.category,m.desc,m.media FROM users AS u INNER JOIN map AS m ON (m.username=u.username) WHERE m.id=(?)
    """,(pid,))
    post = db.fetchall()
    return post






#createTable()