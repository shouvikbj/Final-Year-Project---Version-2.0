import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS follow(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR2(10000),
            following VARCHAR2(10000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS followBackUp AS SELECT * FROM follow WHERE 1=1;
    """)

def entryData(username,following):
    db.execute("INSERT INTO follow VALUES (NULL,?,?)",(username,following))
    db.execute("INSERT INTO followBackUp VALUES (NULL,?,?)",(username,following))
    con.commit()

def getFollowing(username):
    db.execute("SELECT following FROM follow WHERE username=(?)",(username,))
    following = db.fetchall()
    return following

def getFollowingNames(username):
    db.execute("SELECT f.following,u.firstname,u.lastname FROM follow AS f INNER JOIN users AS u ON (f.following=u.username) WHERE f.username=(?)",(username,))
    following = db.fetchall()
    return following

def getFollowers(username):
    db.execute("SELECT username FROM follow WHERE following=(?)",(username,))
    followers = db.fetchall()
    return followers

def getFollowerNames(username):
    db.execute("SELECT f.username,u.firstname,u.lastname FROM follow AS f INNER JOIN users AS u ON (f.username=u.username) WHERE f.following=(?)",(username,))
    followers = db.fetchall()
    return followers

def deleteData(username,following):
    db.execute("DELETE FROM follow WHERE (username=(?) AND following=(?))",(username,following))
    con.commit()




#createTable()

