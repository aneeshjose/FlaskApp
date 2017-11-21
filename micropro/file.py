from flask import Flask, render_template, request,redirect,url_for

import pymysql

con=pymysql.connect(host='localhost',user='root',password='',db='users')
cur=con.cursor()


app=Flask(__name__)

@app.route('/posts',methods=['GET','POST'])
def post():
   if request.method=='POST':
      inp=request.form['thought']
      user='aneesh'
      sql="insert into thoughts values(%s,%s)"
      cur.execute(sql,(user,inp))
      return redirect(url_for('/timeline'))
   return render_template("posts.html",error=None)

if __name__=='__main__':
   app.run()
      
