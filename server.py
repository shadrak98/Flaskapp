from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_mysqldb import MySQL
import yaml
import sys

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def initial():
    return render_template("login.html", error="")

@app.route('/index', methods=['POST'])
def index():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['myemail']
        password = userDetails['mypassword']
        print(str(username))
        ## Verify user details
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user_details where email = %s and password = %s",[str(username), str(password)])
        print("results="+str(result))
        data = str(jsonify(cur.fetchone()))
        print("json"+data)
        print("username"+str(username))
        cur.close()
        print("username"+username)
        if result==1:
            # render_template("index.html")
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE loggedin SET value=1 WHERE email = %s",[str(username)])
            mysql.connection.commit()
            # render_template("index.html")
            res = cursor.execute("SELECT * FROM tasks WHERE email = %s",[username])
            print("res="+str(res))
            if res > 0:
                taskDetails = cursor.fetchall()
                cursor.close()
                return render_template('index.html', taskDetails=taskDetails)
            else:
                # why do we need to check result>0 ?, if there are no tasks, taskDetails will be empty,
                # that wont create any problem
                print("else")
                return render_template("index.html")
        else:
            return render_template("login.html", error="Record not found!")



@app.route('/addtask', methods=['GET', 'POST'])
def addtask():
    cur = mysql.connection.cursor()
    res = cur.execute("SELECT email FROM loggedin where value=1")
    data = cur.fetchone()
    print("addtask res="+str(res))
    print("data"+str(data[0]))
    email = data[0]
    print("email"+str(email))
    cur.close()
    if request.method == 'POST':
        content = request.form.get("myInput")
        # task = content['myInput']
        print("content"+str(request.form.getlist('myInput')))
        print("task="+str(content))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks(email, tasks) VALUES(%s,%s)",[email, content])
        mysql.connection.commit()
        cur.close()
        return render_template("index.html")
        # res = cur.execute("SELECT * FROM tasks where email = %s",[email])
        # print("res in addtask="+str(res))
        # if res > 0:
        #     taskDetails = cur.fetchall()
        #     return render_template('index.html', taskDetails=taskDetails)
        # else:
        #     cur = mysql.connection.cursor()
        #     cur.execute("INSERT INTO tasks(email, tasks) VALUES(%s,%s)",[email, task])
        #     mysql.connection.commit()
        #     cur.close()
        #     return render_template("index.html")
    return render_template("index.html")


@app.route('/register_form')
def register_form():
    return render_template("register_form.html", error='')

@app.route('/logout')
def logout():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE loggedin SET value=0 WHERE value=1")
    mysql.connection.commit()
    cur.close()
    return render_template("login.html")

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['myusername']
        email = userDetails['myemail']
        password = userDetails['mypassword']
        confirmpwd = userDetails['retypepwd']
        if password == confirmpwd:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO user_details(username, email, password) VALUES(%s, %s, %s)",(username, email, password))
            cur.execute("INSERT INTO loggedin(email, value) VALUES(%s, %s)",(email, int(0)))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('addtask'))
        return render_template("register_from.html", error='passwords not matching')
    return render_template('login.html', error="Registration Successfull!")


if __name__ == '__main__':
    app.run(debug=True)