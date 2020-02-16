from flask import Flask,render_template,redirect,request,url_for,session,flash,jsonify
import csv
#import delete as dlt
import loginDB,postDB,blogDB,msgDB,mapDB
import smtplib
import os

app = Flask(__name__, static_url_path='')
app.secret_key = 'this is a secret key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route("/home")
def home():
    if 'username' in session:
        user = loginDB.getUser(session['username'])
        image = user[0][6]
        post = postDB.getAllPost()

        #return render_template("index.html", post=post)
        return render_template("index.html", image=image,post=post)
    else:
        return redirect(url_for('login'))

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    searchbox = request.form.get("text")
    userList = loginDB.getUsers(searchbox)
    return jsonify(userList)

@app.route("/searchUser")
def searchUser():
    if 'username' in session:
        return render_template("searchUser.html")
    else:
        return redirect(url_for('login'))

@app.route("/login", methods = ["POST","GET"])
def login():
    return render_template("login.html")

@app.route("/getin", methods = ["POST","GET"])
def getin():
    username = request.form.get("username")
    password = request.form.get("password")
    details = loginDB.login(username)
    if(username==details[0][0] and password==details[0][1]):
        session['username'] = username
        flash('Successfully logged in !', "success")
        return redirect(url_for('index'))
    else:
        flash('Wrong \"username\" or \"password\"..\nTry again..', "danger")
        return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/register", methods = ["POST","GET"])
def register():
    target = APP_ROOT+'/static/images/profilePics'
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    username = email[:email.find("@")]
    imgfile = request.files.get("img")

    if(imgfile):
        img = imgfile.filename
        destination = "/".join([target,img])
        imgfile.save(destination)
    else:
        img = 'defaultProfileImage.png'
    
    file = open("users.csv","a")
    writer = csv.writer(file)
    file2 = open("users.csv","r")
    reader = csv.reader(file2)
    test = False
    for line in reader:
        if(username == line[0]):
            test = True

    if(test):
        file.close()
        file2.close()
        flash('Provided Email is already in use.\nPlease try with different Email', "warning")
        return  render_template("signup.html")
    
    else:
        writer.writerow((username,firstname,lastname,email,phone,password,img))
        loginDB.createUser(username,firstname,lastname,email,phone,password,img)

        file.close()

        message = "To Login into \"GangPayee\" WebApp \n\nUSERNAME : {}.\n\nRegards from, \nTeam \"GangPayee\""
        message1 = message.format(username)
        message2 = "A new User just registered. \nCheckout."

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('services.shouvikbajpayee@gmail.com', 'MaaThakur60@')
        server.sendmail('services.shouvikbajpayee@gmail.com', email, message1)
        server.sendmail('services.shouvikbajpayee@gmail.com', 'bajpayeeshouvik@gmail.com', message2)
        server.close()

        flash('Your \"Username\" is sent to your registered Email !', "success")
        return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/sendpass", methods = ["POST","GET"])
def sendpassword():
    username = request.form.get("username")
    email = request.form.get("email")
    pnumber = request.form.get("pnumber")
    pswd = loginDB.getPassword(username)
    phone = pswd[0][0]
    password = pswd[0][1]
    msg = "\nLogin credentials for 'GangPayee' :: \nFor Username : '{}' \n Your 'Password' : {}"
    message = msg.format(username,password)
    msg2 = "\nAn user with 'Username' : {} \n Requested 'Password'. \nPlease Check."
    message2 = msg2.format(username)

    if(pnumber == phone):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('services.shouvikbajpayee@gmail.com', 'MaaThakur60@')
        server.sendmail('services.shouvikbajpayee@gmail.com', email, message)
        server.sendmail('services.shouvikbajpayee@gmail.com', 'bajpayeeshouvik@gmail.com', message2)
        server.close()

        return redirect(url_for('login'))
    else:
        return render_template("invalid.html")

@app.route("/account")
def account():
    if 'username' in session:
        user = loginDB.getUser(session['username'])
        #image = "defaultProfileImage.png"
        username = user[0][0]
        firstname = user[0][1]
        lastname = user[0][2]
        email = user[0][3]
        phone = user[0][4]
        password = user[0][5]
        image = user[0][6]
        userPost = postDB.getUserPost(username)
        return render_template("account.html",username=username,firstname=firstname,lastname=lastname,email=email,phone=phone,image=image,password=password,userPost=userPost)
    else:
        return redirect(url_for('login'))

@app.route("/account/<un>")
def userAccount(un):
    if 'username' in session:
        username = session['username']
        if username == un:
            return redirect(url_for('account'))
        else:
            user = loginDB.getUser(un)
            #image = "defaultProfileImage.png"
            username = user[0][0]
            firstname = user[0][1]
            lastname = user[0][2]
            email = user[0][3]
            phone = user[0][4]
            password = user[0][5]
            image = user[0][6]
            userPost = postDB.getUserPost(un)
            return render_template("userAccount.html",username=username,firstname=firstname,lastname=lastname,email=email,phone=phone,image=image,password=password,userPost=userPost)
    else:
        return redirect(url_for('login'))

@app.route("/account/update")
def updateInfo():
    if 'username' in session:
        user = loginDB.getUser(session['username'])
        #image = "defaultProfileImage.png"
        username = user[0][0]
        firstname = user[0][1]
        lastname = user[0][2]
        email = user[0][3]
        phone = user[0][4]
        password = user[0][5]
        image = user[0][6]
        return render_template("updateInfo.html",username=username,firstname=firstname,lastname=lastname,email=email,phone=phone,image=image,password=password)
    else:
        return redirect(url_for('login'))

@app.route("/account/updateDetails", methods = ["POST","GET"])
def updateDetails():
    if 'username' in session:
        target = APP_ROOT+'/static/images/profilePics'
        username = session['username']
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        phone = request.form.get("phone")
        password = request.form.get("password")
        oldpass = loginDB.getPassword(username)
        loginDB.updateDetails(username,firstname,lastname,phone,password)

        file = request.files.get("file")
        if(file):
            filename = file.filename
            destination = "/".join([target,filename])
            file.save(destination)

            loginDB.updateProfilePic(session['username'], filename)
        if(password == oldpass[0][1]):
            flash('Changes successfully saved !',"success")
            return redirect(url_for('account'))
        else:
            flash('Password is changed. Login again !',"warning")
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('login'))


#@app.route("/uploadProfilePic", methods=["POST"])
#def uploadProfilePic():
#    if 'username' in session:
#        target = './static/imges/profilePics'
#        #if not os.path.isdir(target):
#            #os.mkdir(target)
#
#        file = request.files.get("file")
#        if(file):
#            filename = file.filename
#            destination = "/".join([target,filename])
#            file.save(destination)
#
#            loginDB.updateProfilePic(session['username'], filename)
#            
#            dlt.deleteRedundantImages()
#
#            return redirect(url_for('account'))
#        else:
#            return redirect(url_for('account'))
#    else:
#        return redirect(url_for('login'))

@app.route("/postPost", methods=["POST"])
def postQuestion():
    if 'username' in session:
        username = session['username']
        target = APP_ROOT+'/static/posts/postMedia'

        desc = request.form.get("desc")

        media = request.files.get("media")
        
        if (desc == "") and (media.filename == ""):
            flash('Empty post not allowed !',"warning")
            return redirect(url_for('home'))

        media_filename = ""

        if(media):
            media_filename = media.filename
            destination = "/".join([target,media_filename])
            media.save(destination)

        postDB.createPost(username,desc,media_filename)
        flash('Your post is created successfully !',"success")
        return redirect(url_for('home'))

    else:
        return redirect(url_for('login'))

@app.route("/post/<int:pid>")
def post(pid):
    if 'username' in session:
        post = postDB.getPost(pid)
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("post.html", post=post, firstname=firstname, lastname=lastname)
    else:
        return redirect(url_for('login'))

@app.route("/post/<int:pid>/delete", methods=["GET","POST"])
def deletePost(pid):
    if 'username' in session:
        postDB.deletePost(pid)
        flash('Post is deleted !',"success")
        return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))

@app.route("/media/<img>")
def viewMedia(img):
    if 'username' in session:
        media = img
        return render_template("viewMedia.html", media=media)
    else:
        return redirect(url_for('login'))

@app.route("/blog")
def blog():
    if 'username' in session:
        post = blogDB.getAllPost()

        #return render_template("index.html", post=post)
        return render_template("blog.html", post=post)
    else:
        return redirect(url_for('login'))

@app.route("/postBlog", methods=["POST"])
def postBlog():
    if 'username' in session:
        username = session['username']
        desc = request.form.get("desc")
        
        if (desc == ""):
            flash('Empty blog not allowed !',"warning")
            return redirect(url_for('blog'))

        blogDB.createPost(username,desc)
        flash('Your Blog is created successfully !',"success")
        return redirect(url_for('blog'))

    else:
        return redirect(url_for('login'))

@app.route("/blog/<int:pid>")
def blogPost(pid):
    if 'username' in session:
        post = blogDB.getPost(pid)
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("blogPost.html", post=post, firstname=firstname, lastname=lastname)
    else:
        return redirect(url_for('login'))




@app.route("/map")
def map():
    if 'username' in session:
        return render_template("map.html")
    else:
        return redirect(url_for('login'))

@app.route("/getMarkers", methods=["POST","GET"])
def getMarkers():
    posts = mapDB.getAllPosts()
    return jsonify(posts)


@app.route("/report", methods=["GET","POST"])
def report():
    if 'username' in session:
        target = APP_ROOT + '/static/posts/postMedia'

        username = session['username']
        lat = request.form.get("locationLat")
        lng = request.form.get("locationLng")
        category = request.form.get("category")
        desc = request.form.get("desc")
        media = request.files.get("media")

        if (lat == "") or (lng == ""):
            flash('Locations can\'t be empty !',"warning")
            return redirect(url_for('map'))

        media_filename = ""

        if(media):
            media_filename = media.filename
            destination = "/".join([target,media_filename])
            media.save(destination)

        mapDB.createPost(username,lat,lng,category,desc,media_filename)
        flash('Incident reported successfully !',"success")
        return redirect(url_for('map'))

    else:
        return redirect(url_for('login'))


@app.route("/report/<int:pid>")
def viewReport(pid):
    if 'username' in session:
        post = mapDB.getPost(pid)
        return render_template("viewReport.html",post=post)
    else:
        return redirect(url_for('login'))



@app.route("/searchUserforMsg")
def searchUserforMsg():
    if 'username' in session:
        return render_template("searchUserforMsg.html")
    else:
        return redirect(url_for('login'))


@app.route("/msg")
def msgHome():
    if 'username' in session:
        user = session['username']
        msgs = msgDB.getMsgs()
        return render_template("msgHome.html",user=user,msgs=msgs)
    else:
        return redirect(url_for('login'))

@app.route("/sendMsg", methods=["POST","GET"])
def sendMsg():
    if 'username' in session:
        user = session['username']
        msg = request.form.get("msg")
        msgDB.msgEntry(user,msg)
        return redirect(url_for('msgHome'))
    else:
        return redirect(url_for('login'))


#@app.route("/customsearch")
#def customsearch():
#    if 'username' in session:
#        return render_template("customsearch.html")
#    else:
#        return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash('Successfully logged out !', "success")
    return render_template("login.html")
    
    




