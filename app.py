from flask import Flask, render_template, request, redirect, session, url_for
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="collegeinfosystem"
)

# Create a cursor object to interact with the database
cursor = db.cursor()


department = {
    "name": "Computer Science Department",
    "description": "The Computer Science Department is dedicated to the advancement of knowledge in the field of computer science and its applications.",
    "professors": [
        {
            "name": "Professor A",
            "email": "professor_a@example.com",
            "research_interests": ["Machine Learning", "Deep Learning"]
        },
        {
            "name": "Professor B",
            "email": "professor_b@example.com",
            "research_interests": ["Natural Language Processing", "Computer Vision"]
        }
    ]
}

@app.route("/")
def home():
    return render_template("index.html" )

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route("/faculty")
def Faculty():
    return render_template("faculty.html")

@app.route("/students")
def Students():
    # Fetch all students from the database
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('studentscse.html', students=students)

@app.route("/lab")
def Lab():
    return render_template("lab.html")

@app.route("/layout")
def Layout():
    return render_template("layout.html")

@app.route("/cse")
def Cse():
    return render_template("cse.html")

@app.route("/ece")
def Ece():
    return render_template("ece.html")
@app.route("/eee")
def Eee():
    return render_template("eee.html")
@app.route("/ce")
def Ce():
    return render_template("ce.html")

if __name__ == "__main__":
    app.run(debug=True)