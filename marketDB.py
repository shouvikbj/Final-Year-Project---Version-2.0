import sqlite3

con = sqlite3.connect('users.db', check_same_thread=False)
db = con.cursor()

def createTable():
    db.execute("""
        CREATE TABLE IF NOT EXISTS ad(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR2(1000),
            desc VARCHAR2(1000000000000000000),
            phone VARCHAR2(15),
            media VARCHAR2(1000)
        )
    """)
    db.execute("""
    CREATE TABLE IF NOT EXISTS adBackUp AS SELECT * FROM ad WHERE 1=1;
    """)

def createAd(username,desc,phone,media):
    db.execute("INSERT INTO ad VALUES (NULL,?,?,?,?)",(username,desc,phone,media))
    db.execute("INSERT INTO adBackUp VALUES (NULL,?,?,?,?)",(username,desc,phone,media))
    con.commit()

def getAds():
    db.execute("""
        SELECT u.image,u.firstname,u.lastname,p.username,p.id,p.desc,p.phone,p.media FROM users AS u INNER JOIN ad AS p ON (p.username=u.username)
    """)
    ads = db.fetchall()
    return ads

def deleteAd(pid):
    db.execute("DELETE FROM ad WHERE id=(?)",(pid,))
    con.commit()


#createTable()