import pymysql
import time
from flask import Flask,render_template,url_for,make_response,request,redirect,session,flash
conn=pymysql.connect(host='localhost',user='root',password='',db='users')
cur=conn.cursor()
app=Flask(__name__)
app.secret_key='secret key'
@app.route('/login', methods=['GET','POST'])
def login():
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    error = None
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
        cur.close()
    return render_template("login.html", error=error)
@app.route('/welcome')
def welcome():
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    try:
        session_id=session['user_id']
        session_val=session['sufficient']
    except (KeyError):
        return redirect(url_for('login'))
    if session_id:
        sql6="select username,thought from thoughts order by time desc"
        cur.execute(sql6)
        thou=cur.fetchall()
        user1=thou[0][0]
        thought1=thou[0][1]
        user2=thou[1][0]
        t2=thou[1][1]
        u3=thou[2][0]
        t3=thou[2][1]
        return render_template('welcome.html',u1=user1,t1=thought1,u2=user2,t2=t2,u3=u3,t3=t3) 


    
    else:
        return "please sign in"
    cur.close()
@app.route('/logout')
def logout():
    session['user_id']=None
    return redirect(url_for('login'))

@app.route('/post',methods=['POST','GET'])
def post():
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    if request.method=='POST':
        userna=session['user_id']
        postcontent=request.form['thoughts']
        times=time.strftime('%Y%m%d%H%M%S')
        sql5="insert into thoughts values(%s,%s,%s)"
        cur.execute(sql5,(userna,postcontent,times))
        return redirect(url_for('welcome'))
    cur.c;ose()
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
    cur.close()
    return render_template('find.html',user1=user1,user2=user2,user3=user3,user4=user4)
if __name__=='__main__':
    app.run()
