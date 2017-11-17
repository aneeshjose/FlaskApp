import pymysql
import time
from flask import Flask,render_template,url_for,make_response,request,redirect,session,flash
conn=pymysql.connect(host='localhost',user='root',password='',db='users')
cur=conn.cursor()
app=Flask(__name__)
app.secret_key='secret key'

@app.route('/')
def index():
    try:
        if  session['user_id']:
            return redirect(url_for('welcome'))
    except (KeyError):
        return redirect(url_for('login'))
    
@app.route('/login', methods=['GET','POST'])
def login():
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    if request.method == 'POST':
        user=request.form['username']
        passw=request.form['password']
        sql=('select username,password from users where username=%s and password=%s')
        cur.execute(sql,(user,passw))
        login=cur.fetchone()
        if login[0]==user and passw==login[1]:
            session['user_id'] = user
            session['sufficient']=passw
            flash("You were Logged In")
            return redirect(url_for('welcome'))
        else:
            error=None
            return error
    conn.close()
    return render_template("login.html")
@app.route('/welcome')
def welcome():
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    try:
        if not session['user_id']:
            return redirect(url_for('login'))
    except (KeyError):
        return redirect(url_for('login'))
    cur.execute("select username,thought from thoughtss order by times desc")
    a=cur.fetchall()
    user=[0]*len(a)
    thought=[0]*len(a)
    for i in range(len(a)):
        user[i]=a[i][0]
        thought[i]=a[i][1]
    leng=len(user)  
    cur.close()
    return render_template('welcome.html',leng=leng,user=user,thought=thought)
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

@app.route('/post',methods=['POST','GET'])
def post():
    try:
        if not session['user_id']:
            return True
    except (KeyError):
        return redirect(url_for('login'))
        conn=pymysql.connect(host='localhost',user='root',password='',db='users')
        cur=conn.cursor()
        if request.method=='POST':
            userna=session['user_id']
            postcontent=request.form['thoughts']
            times=time.strftime('%Y%m%d%H%M%S')
            sql5="insert into thoughtss values(%s,%s,%s)"
            cur.execute(sql5,(userna,postcontent,times))
            return redirect(url_for('welcome'))
        conn.close()
    return render_template('posts.html')

@app.route('/find-friends',methods=['GET','POST'])
def find():
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    sqlfindfriends="select username from users"
    cur.execute(sqlfindfriends)
    a=cur.fetchall()
    user1=a[0][0]
    user2=a[1][0]
    user3=a[2][0]
    user4=a[3][0]
    conn.close()                      
    conn.close()
    return render_template('find.html',user1=user1,user2=user2,user3=user3,user4=user4)
@app.route('/signup',methods=['GET','POST'])
def signup():
    try:
        if session['user_id']:
            return redirect(url_for('welcome'))
    except (KeyError):
        conn=pymysql.connect(host='localhost',user='root',password='',db='users')
        cur=conn.cursor()
        if request.method=="POST":
            username=request.form['username']
            passw=request.form['password']
            sqlinsert='insert into users values(%s,%s)'
            a=cur.execute(sqlinsert,(username,passw))
            if a==1:
                session['user_id']=username
                session['sufficient']=passw
                return redirect(url_for('welcome'))
            else:
                return "Cannot add you "
        else:
            return redirect(url_for('welcome'))
        conn.close()
    return render_template('signup.html')

if __name__=='__main__':
    app.run()
