import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS blogLike(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid INTEGER,
            username VARCHAR2(1000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS blogLikeBackUp AS SELECT * FROM blogLike WHERE 1=1;
    """)

def like(pid,username):
    db.execute("INSERT INTO blogLike VALUES (NULL,?,?)",(pid,username))
    db.execute("INSERT INTO blogLikeBackUp VALUES (NULL,?,?)",(pid,username))
    con.commit()


def dislike(pid,username):
    db.execute("DELETE FROM blogLike WHERE pid=(?) AND username=(?)",(pid,username))
    con.commit()

def dislikeAll(pid):
    db.execute("DELETE FROM blogLike WHERE pid=(?)",(pid,))
    con.commit()

def getLikes(pid):
    db.execute("SELECT COUNT(id) FROM blogLike WHERE pid=(?)",(pid,))
    likes = db.fetchall()
    return likes

def usersLiked(pid):
    db.execute("SELECT username FROM blogLike WHERE pid=(?)",(pid,))
    likedUsers = db.fetchall()
    return likedUsers






#createTable()