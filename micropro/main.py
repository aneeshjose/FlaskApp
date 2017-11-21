import pymysql
import time
from flask import Flask,render_template,url_for,make_response,request,redirect,session,flash
app=Flask(__name__)
app.secret_key='secret key'

@app.route('/',methods=['GET','POST'])
def index():
    try:
        if  session['user_id']:
            return redirect(url_for('welcome'))
    except (KeyError):
        conn=pymysql.connect(host='localhost',user='root',password='',db='users')
        cur=conn.cursor()
        if request.method=='POST':
            try:
                user=request.form['username']
                passwo=request.form['password']
                sqluserinsert="insert into users values(%s,%s)"
                cur.execute(sqluserinsert,(user,passwo))
                session['user_id']=user
                return redirect(url_for('welcome'))
            except (TypeError):
                return redirect(url_for('/'))
        conn.close()
    return render_template('signup.html')
        
    
@app.route('/login', methods=['GET','POST'])
def login():
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    if request.method == 'POST':
        try:
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
        except (TypeError):
            return redirect(url_for('login'))
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
    cur.execute("select username,thought,times from thoughtss order by times desc")
    a=cur.fetchall()
    user=[0]*len(a)
    thought=[0]*len(a)
    times=[0]*len(a)
    table=[0]*len(a)
    likes2=[0]*len(a)
    happy2=[0]*len(a)
    angry2=[0]*len(a)
    love2=[0]*len(a)
    ll=len(a)
    sqllikes=[0]*ll
    sqlangry=[0]*ll
    sqlhappy=[0]*ll
    sqlloves=[0]*ll
    for i in range(len(a)):
        user[i]=a[i][0]
        thought[i]=a[i][1]
        times[i]=a[i][2]
        table[i]=user[i]+"_"+times[i]
        sqllikes[i]="select count(likes) from "+table[i]
        cur.execute(sqllikes[i])
        sqllikes[i]=cur.fetchone()[0]
        sqlangry[i]="select count(angry) from "+table[i]
        cur.execute(sqlangry[i])
        sqlangry[i]=cur.fetchone()[0]
        sqlhappy[i]="select count(happy) from "+table[i]
        cur.execute(sqlhappy[i])
        sqlhappy[i]=cur.fetchone()[0]
        sqlloves[i]="select count(love) from "+table[i]
        cur.execute(sqlloves[i])
        sqlloves[i]=cur.fetchone()[0]
    leng=len(user)
    
    
    conn.close()
    return render_template('welcome.html',likes=sqllikes,loves=sqlloves,angry=sqlangry,happy=sqlhappy,table=table,leng=leng,user=user,thought=thought,times=times)
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('signup'))

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
        table2=userna+"_"+times
        sql5="insert into thoughtss values(%s,%s,%s)"
        cur.execute(sql5,(userna,postcontent,times))
        sqlcreate="create table "+table2+" (likes varchar(30),happy varchar(30),love varchar(40),angry varchar(40))"
        cur.execute(sqlcreate)
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
@app.route('/like/<times>')
def like(times):
    try:
        if not session['user_id']:
            return redirect(url_for('login'))
    except (KeyError):
        return redirect(url_for('login'))
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    
    user=session['user_id']
    
    table=user+"_"+times
    sqllike="insert into "+table+" (likes) values(%s)"
    sqluser='select username from thoughtss where times=%s'
    cur.execute(sqluser,(times))
    user1=cur.fetchone()
    users=user1[0]
    table=users+"_"+times
    sqllike="insert into "+table+" (likes) values(%s)"
    sqllikecheck='select likes from  '+table+' where likes=%s'
    n=cur.execute(sqllikecheck,(user))
    if n==0:
        cur.execute(sqllike,(user))
    else:
        x='UPDATE '+table+' set likes=null where likes=%s'
        cur.execute(x,(user))
    conn.close()
    return redirect(url_for('welcome'))

@app.route('/happy/<times>')
def happy(times):
    try:
        if not session['user_id']:
            return redirect(url_for('login'))
    except (KeyError):
        return redirect(url_for('login'))
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    
    user=session['user_id']
    
    table=user+"_"+times
    sqllike="insert into "+table+" (happy) values(%s)"
    sqluser='select username from thoughtss where times=%s'
    cur.execute(sqluser,(times))
    user1=cur.fetchone()
    users=user1[0]
    table=users+"_"+times
    sqllike="insert into "+table+" (happy) values(%s)"
    sqllikecheck='select happy from  '+table+' where happy=%s'
    n=cur.execute(sqllikecheck,(user))
    if n==0:
        cur.execute(sqllike,(user))
    else:
        x='UPDATE '+table+' set happy=null where happy=%s'
        cur.execute(x,(user))
    conn.close()
    return redirect(url_for('welcome'))    

@app.route('/love/<times>')
def love(times):
    try:
        if not session['user_id']:
            return redirect(url_for('login'))
    except (KeyError):
        return redirect(url_for('login'))
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    
    user=session['user_id']
    
    table=user+"_"+times
    sqllike="insert into "+table+" (love) values(%s)"
    sqluser='select username from thoughtss where times=%s'
    cur.execute(sqluser,(times))
    user1=cur.fetchone()
    users=user1[0]
    table=users+"_"+times
    sqllike="insert into "+table+" (love) values(%s)"
    sqllikecheck='select love from  '+table+' where love=%s'
    n=cur.execute(sqllikecheck,(user))
    if n==0:
        cur.execute(sqllike,(user))
    else:
        x='UPDATE '+table+' set love=null where love=%s'
        cur.execute(x,(user))
    conn.close()
    return redirect(url_for('welcome'))


@app.route('/angry/<times>')
def angry(times):
    try:
        if not session['user_id']:
            return redirect(url_for('login'))
    except (KeyError):
        return redirect(url_for('login'))
    conn=pymysql.connect(host='localhost',user='root',password='',db='users')
    cur=conn.cursor()
    
    user=session['user_id']
    sqluser='select username from thoughtss where times=%s'
    cur.execute(sqluser,(times))
    user1=cur.fetchone()
    users=user1[0]
    table=users+"_"+times
    sqllike="insert into "+table+" (angry) values(%s)"
    sqllikecheck='select angry from  '+table+' where angry=%s'
    n=cur.execute(sqllikecheck,(user))
    if n==0:
        cur.execute(sqllike,(user))
    else:
        x='UPDATE '+table+' set angry=null where angry=%s'
        cur.execute(x,(user))
    conn.close()
    return redirect(url_for('welcome'))       

if __name__=='__main__':
    app.run()
