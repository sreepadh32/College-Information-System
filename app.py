from email import message
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

studentdelmsg=""
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
    return render_template("index.html",user=0 )

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<      admin portal        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route("/admin")
def Admin():
    return render_template("adminportal.html",user=session['user_id'])
#add user
@app.route("/adduser", methods=['GET','POST'])
def AddUser():
    if request.method == "POST":
        username= request.form['newusername']
        password= request.form["newpassword"]
        is_admin= request.form.get('isadmin')
        if is_admin:  # If the checkbox is checked, is_admin will be 'on'
            cursor.execute("INSERT INTO `admins` (`adminid`, `username`, `password`) VALUES (NULL, %s, %s);", (username,password))
            db.commit()
            return render_template("adduser.html",message='Added new admin')
        else:
            cursor.execute("INSERT INTO `users` (`userid`, `username`, `password`) VALUES (NULL, %s, %s);", (username,password))
            db.commit()
            return render_template("adduser.html",message='Added new user')
    return render_template("adduser.html")

@app.route("/deleteuser")
def DeleteUser():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()
    return render_template("deleteuser.html", users=users, admins=admins)

@app.route("/deluser/<uid>")
def DelUser(uid):
    cursor.execute("DELETE FROM users WHERE userid= %s;", (uid,))
    db.commit()
    return redirect("/deleteuser")

@app.route("/deladmin/<uid>")
def DelAdmin(uid):
    cursor.execute("DELETE FROM admins WHERE adminid = %s;", (uid,))
    db.commit()
    return redirect("/deleteuser")

@app.route("/addstudent", methods=['GET', 'POST'])
def AddStudent():
    if request.method == "POST":
        university_id = request.form['university_id']
        name = request.form['name']
        batch = request.form['batch']
        department = request.form['department']

        cursor.execute("SELECT * FROM students WHERE uniID= %s;", (university_id,))
        student = cursor.fetchone()

        if student:
            return render_template("addstudent.html", errmessage="Error: Student already exists")
        else:
            cursor.execute("INSERT INTO `students` (`uniID`, `name`, `batch`, `dept`) VALUES (%s,%s,%s,%s);", (university_id,name,batch,department))
            db.commit()
            return render_template("addstudent.html", message='Student added successfully')
    return render_template("addstudent.html")

@app.route("/deletestudent", methods=['GET', 'POST'])
def deleteStudent():
    if request.method == "POST":
        university_id = request.form['university_id']
        cursor.execute("SELECT * FROM students WHERE uniID= %s;", (university_id,))
        student = cursor.fetchall()

        if student:
            return render_template("deletestudent.html", students=student)
        else:
            return render_template("deletestudent.html", message='NO student found')
    elif request.method == "GET":
        message = request.args.get("message")
        return render_template("deletestudent.html", message=message)
    return render_template("deletestudent.html") 
@app.route("/delstud/<uid>")
def DelStud(uid):
    cursor.execute("DELETE FROM students WHERE uniID = %s;", (uid,))
    db.commit()
    return redirect(url_for("deleteStudent", message="Student Deletion Succesfull"))


@app.route("/addfaculty", methods=['GET', 'POST'])
def AddFaculty():
    if request.method == "POST":
        name = request.form['name']
        department = request.form['department']
        doj = request.form['doj']
        email = request.form['email']
        mobile = request.form['mobile']
        qualification = request.form['qualification']
        experience = request.form['experience']
        intrest = request.form['intrest']
        desig = request.form['desig']

        cursor.execute("SELECT * FROM faculties WHERE name= %s;", (name,))
        student = cursor.fetchone()

        if student:
            return render_template("addfaculty.html", errmessage="Error: Faculty already exists")
        else:
            cursor.execute("INSERT INTO `faculties` ( `name`, `department`, `doj`, `mailid`, `mobile`, `qualification`, `experience`, `intrest`, `designation`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,department,doj,email,mobile,qualification,experience,intrest,desig))
            db.commit()
            return render_template("addfaculty.html", message='Faculty added successfully')
    return render_template("addfaculty.html")

@app.route("/deletefaculty", methods=['GET', 'POST'])
def deleteFaculty():
    if request.method == "POST":
        dept = request.form['department']
        cursor.execute("SELECT * FROM faculties WHERE department LIKE %s ORDER BY facultyID;", ('%'+dept+'%',))
        faculty = cursor.fetchall()
        if faculty:
            return render_template("deletefaculty.html", faculties=faculty)
        else:
            return render_template("deletefaculty.html", message='NO Faculty found')
    elif request.method == "GET":
        message = request.args.get("message")
        return render_template("deletefaculty.html", message=message)
    return render_template("deletefaculty.html") 
@app.route("/delfacul/<uid>")
def DelFacul(uid):
    cursor.execute("DELETE FROM faculties WHERE facultyID = %s;", (uid,))
    db.commit()
    return redirect(url_for("deleteFaculty", message="Faculty Deletion Succesfull"))

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<      login page        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid user
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        # Check if the username and password are valid admin
        cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
        admin = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return render_template("index.html",user=user[1] )
        elif admin:
            session['user_id'] = admin[0]
            return render_template("adminportal.html",user=admin[1] )
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<      faculties pages        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route("/faculty")
def Faculty():
    cursor.execute("SELECT * FROM faculties ORDER BY facultyID;")
    faculties = cursor.fetchall()
    return render_template("faculty.html", faculties=faculties)

@app.route("/facultycse")
def FacultyCSE():
    cursor.execute("SELECT * FROM faculties WHERE department LIKE %s ORDER BY facultyID;", ('%CSE%',))
    faculties = cursor.fetchall()
    return render_template("facultycse.html", faculties=faculties)

@app.route("/facultyce")
def FacultyCE():
    cursor.execute("SELECT * FROM faculties WHERE department LIKE %s ORDER BY facultyID;", ('CE',))
    faculties = cursor.fetchall()
    return render_template("facultyce.html", faculties=faculties)

@app.route("/facultyece")
def FacultyECE():
    cursor.execute("SELECT * FROM faculties WHERE department LIKE %s ORDER BY facultyID;", ('%ECE%',))
    faculties = cursor.fetchall()
    return render_template("facultyece.html", faculties=faculties)

@app.route("/facultyeee")
def FacultyEEE():
    cursor.execute("SELECT * FROM faculties WHERE department LIKE %s ORDER BY facultyID;", ('%EEE%',))
    faculties = cursor.fetchall()
    return render_template("facultyeee.html", faculties=faculties)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<      students pages        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.route("/students")
def Students():
    # Fetch all students from the database
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('students.html', students=students)

@app.route("/studentscse")
def StudentsCSE():
    # Fetch all students from the database
    cursor.execute("SELECT * FROM students  WHERE dept LIKE %s ORDER BY uniID;", ('%CS%',))
    students = cursor.fetchall()
    return render_template('studentscse.html', students=students)

@app.route("/studentsece")
def StudentsECE():
    # Fetch all students from the database
    cursor.execute("SELECT * FROM students  WHERE dept LIKE 'ECE' ORDER BY uniID;")
    students = cursor.fetchall()
    return render_template('studentsece.html', students=students)

@app.route("/studentsce")
def StudentsCE():
    # Fetch all students from the database
    cursor.execute("SELECT * FROM students  WHERE dept LIKE 'CE' ORDER BY uniID;")
    students = cursor.fetchall()
    return render_template('studentsce.html', students=students)

@app.route("/studentseee")
def StudentsEEE():
    # Fetch all students from the database
    cursor.execute("SELECT * FROM students  WHERE dept LIKE 'EEE' ORDER BY uniID;")
    students = cursor.fetchall()
    return render_template('studentseee.html', students=students)

@app.route("/lab")
def Lab():
    return render_template("lab.html")

@app.route("/layout")
def Layout():
    return render_template("layout.html")

@app.route("/clglayout")
def CLGLayout():
    return render_template("clglayout.html")

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