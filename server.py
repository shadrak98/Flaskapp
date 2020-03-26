from flask import Flask, render_template, redirect, request, url_for
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

        ## Verify user details
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM user_details where email = %s and password = %s",(username, password))
        # result=0
        # if password=="1": result=1
        print(str(result))
        # app.logger.debug(result)
        if result==1:
            # return render_template("index.html")
            cur = mysql.connection.cursor()
            res = cur.execute("SELECT * FROM tasks where email = %s", (username))
            if res > 0:
                taskDetails = cur.fetchall()
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
    # em = var
    # print(em)
    email = request.args.get('var')
    if request.method == 'POST':
        content = request.form
        task = content['myInput']
        print(content["myInput"])
        cur = mysql.connection.cursor()
        res = cur.execute("SELECT * FROM tasks where email = %s",(email))
        if res > 0:
            taskDetails = cur.fetchall()
            return render_template('index.html', taskDetails=taskDetails)
        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tasks(email, tasks) VALUES(%s,%s)",(email, task))
            mysql.connection.commit()
            cur.close()
            return render_template("index.html")
    return render_template("index.html")


@app.route('/register_form')
def register_form():
    return render_template("register_form.html", error='')

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
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('addtask', var=email))
        return render_template("register_from.html", error='passwords not matching')
    return render_template('login.html', error="Registration Successfull!")


if __name__ == '__main__':
    app.run(debug=True)