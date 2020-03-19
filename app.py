from flask import Flask,render_template,redirect,request,url_for,session,flash,jsonify,make_response
import csv
#import delete as dlt
import loginDB,postDB,blogDB,msgDB,mapDB,commentDB,blogCommentDB,likeDB,blogLikeDB
import smtplib
import os

app = Flask(__name__, static_url_path='')
app.secret_key = 'this is a secret key'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    #if ('username' in session):
    #    return redirect(url_for('home'))
    if request.cookies.get('username'):
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route("/home")
def home():
    #if 'username' in session:
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        user = loginDB.getUser(request.cookies.get('username'))
        image = user[0][6]
        post = postDB.getAllPost()
        resp = make_response(render_template("index.html", image=image,post=post))
        #return render_template("index.html", post=post)
        #return render_template("index.html", image=image,post=post)
        return resp
    else:
        return redirect(url_for('login'))

@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    searchbox = request.form.get("text")
    userList = loginDB.getUsers(searchbox)
    return jsonify(userList)

@app.route("/searchUser")
def searchUser():
    if request.cookies.get('username'):
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
    if(len(details)):
        if(username==details[0][0] and password==details[0][1]):
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('username', username, max_age=60*60*24*365*2)
            #session['username'] = username
            flash('Successfully logged in !', "success")
            #return redirect(url_for('index'))
            return resp
        else:
            flash('Wrong \"username\" or \"password\"..\nTry again..', "danger")
            return redirect(url_for('login'))
    elif(username=="admin" and password=="gangpayee@gcetts"):
        session['username'] = "Admin"
        return redirect(url_for('admin'))
    
    else:
            flash('Wrong \"username\" or \"password\"..\nTry again..', "danger")
            return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if 'username' in session:
        if (session['username']=="Admin"):
            users = loginDB.getAll()
            return render_template("admin.html",users=users)
        else:
            flash("Admin access needed.","warning")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

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
        message = "To Login into \"GangPayee\" WebApp \n\nUSERNAME : {}\n\nRegards from, \nTeam \"GangPayee\""
        message1 = message.format(username)
        message2 = "A new User just registered. \nCheckout :\nhttps://gangpayee.herokuapp.com/admin"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('services.shouvikbajpayee@gmail.com', 'mAAtHAKUR60@')
        server.sendmail('services.shouvikbajpayee@gmail.com', email, message1)
        server.sendmail('services.shouvikbajpayee@gmail.com', 'bajpayeeshouvik@gmail.com', message2)
        server.close()

        writer.writerow((username,firstname,lastname,email,phone,password,img))
        loginDB.createUser(username,firstname,lastname,email,phone,password,img)

        file.close()

        flash('Your \"Username\" is sent to your registered Email !', "success")
        return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot.html")

@app.route("/sendpass", methods=["POST","GET"])
def sendpassword():
    username = request.form.get("username")
    email = request.form.get("email")
    pnumber = request.form.get("phone")
    pswd = loginDB.getPassword(username)
    if (len(pswd)==0):
        flash('Wrong username. Try again with correct \'username\'',"warning")
        return redirect(url_for('forgot'))
    phone = pswd[0][0]
    password = pswd[0][1]
    username1 = pswd[0][2]
    email1 = pswd[0][3]
    #msg = "\nLogin credentials for 'GangPayee' :: \nFor Username : '{}' \n Your 'Password' : {}"
    #message = msg.format(username,password)
    msg2 = "\nAn user with 'Username' : {} \nRequested 'Password'. \nTo confirm, click the link below:\nhttps://gangpayee.pythonanywhere.com/sendpass/{}/{}/{}/grant"
    message2 = msg2.format(username,username,email,phone)

    if((pnumber==phone) and (email==email1)):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login('services.shouvikbajpayee@gmail.com', 'mAAtHAKUR60@')
        #server.sendmail('services.shouvikbajpayee@gmail.com', email, message)
        server.sendmail('services.shouvikbajpayee@gmail.com', 'bajpayeeshouvik@gmail.com', message2)
        server.close()
        flash('Password will be sent to your Registered Email after the verification of your request.',"success")
        return redirect(url_for('login'))
    else:
        flash('Provided credentials didn\'t match ! Try again.',"warning")
        return redirect(url_for('forgot'))

@app.route("/sendpass/<username>/<email>/<phone>/grant")
def grantPassword(username,email,phone):
    username = username
    email = email
    pnumber = phone
    pswd = loginDB.getPassword(username)
    phone = pswd[0][0]
    password = pswd[0][1]
    msg = "\nLogin credentials for 'GangPayee' :: \nFor Username : '{}' \nYour 'Password' : {}"
    message = msg.format(username,password)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login('services.shouvikbajpayee@gmail.com', 'mAAtHAKUR60@')
    server.sendmail('services.shouvikbajpayee@gmail.com', email, message)
    #server.sendmail('services.shouvikbajpayee@gmail.com', 'bajpayeeshouvik@gmail.com', message2)
    server.close()
    flash('Password is sent to user.',"success")
    return redirect(url_for('login'))


@app.route("/account")
def account():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        user = loginDB.getUser(request.cookies.get('username'))
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
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
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

@app.route("/account/<un>/delete")
def deleteUser(un):
    if 'username' in session:
        if (session['username'] == "Admin"):
            loginDB.deleteUser(un)
            return redirect(url_for('admin'))
        else:
            flash('Admin access needed to perform this operation.!\nUnauthorised access reported to Admins..',"danger")
            return redirect(url_for('logout'))
    else:
        return redirect(url_for('login'))

@app.route("/account/update")
def updateInfo():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        user = loginDB.getUser(request.cookies.get('username'))
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
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        target = APP_ROOT+'/static/images/profilePics'
        username = request.cookies.get('username')
        #username = session['username']
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

            loginDB.updateProfilePic(request.cookies.get('username'), filename)
        if(password == oldpass[0][1]):
            flash('Changes successfully saved !',"success")
            return redirect(url_for('account'))
        else:
            flash('Changes saved successfully.\nPassword is changed. Login again !',"warning")
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
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
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
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        user = request.cookies.get('username')
        post = postDB.getPost(pid)
        comments = commentDB.getComments(pid)
        likes = likeDB.getLikes(pid)
        likedUsers = likeDB.usersLiked(pid)
        no_likes = likes[0][0]
        #print(likedUsers)
        #print(comments)
        #user = session['username']
        liked = 0
        for i in range(len(likedUsers)):
            if user in likedUsers[i][0]:
                liked = 1

        postid = post[0][6]
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("post.html", liked=liked, no_likes=no_likes, post=post, user=user, firstname=firstname, lastname=lastname, postid=postid, comments=comments)
    else:
        post = postDB.getPost(pid)
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("post2.html", post=post, firstname=firstname, lastname=lastname)

@app.route("/post/<int:pid>/comment",methods=["POST","GET"])
def comment(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        comment = request.form.get("commentBox")
        commentDB.addComment(pid,username,comment)
        redirectUrl = '/post/'+str(pid)
        flash('comment posted',"success")
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))



@app.route("/post/<int:pid>/like")
def like(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        likeDB.like(pid,username)
        redirectUrl = '/post/'+str(pid)
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))


@app.route("/post/<int:pid>/dislike")
def dislike(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        likeDB.dislike(pid,username)
        redirectUrl = '/post/'+str(pid)
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))





@app.route("/post/<int:pid>/comment/<int:cid>/delete",methods=["POST","GET"])
def deleteComment(pid,cid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        commentDB.deleteComment(pid,cid)
        redirectUrl = '/post/'+str(pid)
        flash('comment deleted',"warning")
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))


@app.route("/post/<int:pid>/delete", methods=["GET","POST"])
def deletePost(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        likeDB.dislikeAll(pid)
        commentDB.deleteAllComment(pid)
        postDB.deletePost(pid)
        flash('Post is deleted !',"success")
        return redirect(url_for('account'))
    else:
        return redirect(url_for('login'))

@app.route("/media/<img>")
def viewMedia(img):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        loggedin = 1
        media = img
        return render_template("viewMedia.html", media=media, loggedin=loggedin)
    else:
        media = img
        return render_template("viewMedia.html", media=media)

@app.route("/dp/<img>")
def viewDp(img):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        media = img
        return render_template("viewDp.html", media=media)
    else:
        return redirect(url_for('login'))

@app.route("/blog")
def blog():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        user = request.cookies.get('username')
        post = blogDB.getAllPost()
        #user = session['username']
        return render_template("blog.html", post=post,user=user)
    else:
        return redirect(url_for('login'))


@app.route("/blog/<int:pid>/comment",methods=["POST","GET"])
def blogComment(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        comment = request.form.get("commentBox")
        blogCommentDB.addblogComment(pid,username,comment)
        redirectUrl = '/blog/'+str(pid)
        flash('comment posted',"success")
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))


@app.route("/blog/<int:pid>/comment/<int:cid>/delete",methods=["POST","GET"])
def deleteblogComment(pid,cid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        blogCommentDB.deleteblogComment(pid,cid)
        redirectUrl = '/blog/'+str(pid)
        flash('comment deleted',"warning")
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))



@app.route("/blog/<int:pid>/like")
def blogLike(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        blogLikeDB.like(pid,username)
        redirectUrl = '/blog/'+str(pid)
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))


@app.route("/blog/<int:pid>/dislike")
def blogDislike(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        blogLikeDB.dislike(pid,username)
        redirectUrl = '/blog/'+str(pid)
        return redirect(redirectUrl)
    else:
        return redirect(url_for('login'))




@app.route("/blog/<int:pid>/delete", methods=["GET","POST"])
def deleteblogPost(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        blogLikeDB.dislikeAll(pid)
        blogCommentDB.deleteAllComment(pid)
        blogDB.deletePost(pid)
        flash('Post is deleted !',"success")
        return redirect(url_for('blog'))
    else:
        return redirect(url_for('login'))



@app.route("/postBlog", methods=["POST"])
def postBlog():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
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
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        user = request.cookies.get('username')
        post = blogDB.getPost(pid)
        comments = blogCommentDB.getblogComments(pid)
        likes = blogLikeDB.getLikes(pid)
        likedUsers = blogLikeDB.usersLiked(pid)
        no_likes = likes[0][0]
        #print(likedUsers)
        #print(comments)
        #user = session['username']
        liked = 0
        for i in range(len(likedUsers)):
            if user in likedUsers[i][0]:
                liked = 1

        postid = post[0][5]
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("blogPost.html", liked=liked, no_likes=no_likes, post=post, firstname=firstname, lastname=lastname,user=user,postid=postid,comments=comments)
    else:
        post = blogDB.getPost(pid)
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("blogPost2.html", post=post, firstname=firstname, lastname=lastname)




@app.route("/map")
def map():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        return render_template("map.html")
    else:
        return redirect(url_for('login'))

@app.route("/getMarkers", methods=["POST","GET"])
def getMarkers():
    posts = mapDB.getAllPosts()
    return jsonify(posts)


@app.route("/report", methods=["GET","POST"])
def report():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        target = APP_ROOT + '/static/posts/postMedia'
        username = request.cookies.get('username')

        #username = session['username']
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
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        post = mapDB.getPost(pid)
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("viewReport.html",post=post,user=user,firstname=firstname,lastname=lastname)
    else:
        user = ""
        post = mapDB.getPost(pid)
        firstname = post[0][1]
        lastname = post[0][2]
        return render_template("viewReport.html",post=post,user=user,firstname=firstname,lastname=lastname)


@app.route("/report/<int:pid>/delete", methods=["POST","GET"])
def deleteReport(pid):
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        mapDB.deleteReport(pid)
        flash('Incident Report deleted !',"success")
        return redirect(url_for('map'))
    else:
        return redirect(url_for('login'))



@app.route("/searchUserforMsg")
def searchUserforMsg():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        return render_template("searchUserforMsg.html")
    else:
        return redirect(url_for('login'))


@app.route("/msg")
def msgHome():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        msgs = msgDB.getMsgs()
        return render_template("msgHome.html",user=user,msgs=msgs)
    else:
        return redirect(url_for('login'))

@app.route("/sendMsg", methods=["POST","GET"])
def sendMsg():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        username = request.cookies.get('username')
        msg = request.form.get("msg")
        msgDB.msgEntry(user,msg)
        return redirect(url_for('msgHome'))
    else:
        return redirect(url_for('login'))



@app.route("/notification")
def notification():
    if request.cookies.get('username'):
        #user = loginDB.getUser(session['username'])
        #username = loginDB.getUser(request.cookies.get('username'))
        return render_template("notification.html")
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
    #session.pop('username', None)
    #flash('Successfully logged out !', "success")
    #return render_template("login.html")
    username = loginDB.getUser(request.cookies.get('username'))
    resp = make_response(render_template("login.html"))
    resp.set_cookie('username', expires=0)
    #resp.delete_cookie('username', path='/login', domain='127.0.0.1:5002')
    return resp
    
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=True)



