from flask import Flask, render_template, request,session
from datetime import date
import ibm_boto3
import os
from ibm_botocore.client import Config, ClientError

app = Flask(__name__)
app.secret_key ='a'
def showall():
    sql= "SELECT * from USER"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ",  dictionary["CONTACT"])
        print("The Adress is : ",  dictionary["ADDRESS"])
        print("The Role is : ",  dictionary["ROLE"])
        print("The Branch is : ",  dictionary["BRANCH"])
        print("The Password is : ",  dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def getdetails(email,password):
    sql= "select * from MY_TABLE where email='{}' and password='{}'".format(email,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary != False:
        print("The Name is : ",  dictionary["NAME"])
        print("The E-mail is : ", dictionary["EMAIL"])
        print("The Contact is : ", dictionary["CONTACT"])
        print("The Address is : ", dictionary["ADDRESS"])
        print("The Role is : ", dictionary["ROLE"])
        print("The Branch is : ", dictionary["BRANCH"])
        print("The Password is : ", dictionary["PASSWORD"])
        dictionary = ibm_db.fetch_both(stmt)
        
def insertdb(conn,usn,name,branch,semester,email,phone,password):
    sql= "INSERT into STUDENT VALUES('{}','{}','{}','{}','{}','{}','{}')".format(usn,name,branch,semester,email,phone,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))
    
def insertfaculty(conn,name,designation,branch,email,phone,password):
    sql= "INSERT into FACULTY VALUES('{}','{}','{}','{}','{}','{}')".format(name,designation,branch,email,phone,password)
    stmt = ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))    
    
import ibm_db
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=fbd88901-ebdb-4a4f-a32e-9822b9fb237b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32731;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=wbj37866;PWD=1RztLEHwRBEgrMb1",'','')
print(conn)
print("connection successful...")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/facultyreg', methods=['POST','GET'])
def facultyreg():
    return render_template('facultyreg.html')

@app.route('/registration', methods=['POST','GET'])
def registration():
    return render_template('registration.html')

@app.route('/adminreg', methods=['POST', 'GET'])
def adminreg():
    return render_template('adminreg.html')

@app.route('/createassignment', methods=['POST','GET'])
def createassignment():
    if request.method== "POST":
        email = request.form["email"]
        assign_no = request.form["assign_no"]
        title = request.form["title"]
        description = request.form["desc"]
        s_date = request.form["s_date"]
        e_date = request.form["e_date"]
        
        sql="INSERT into ASSIGNMENT VALUES('{}','{}','{}','{}','{}','{}')".format(assign_no, title, description, s_date, e_date, email)
        stmt = ibm_db.exec_immediate(conn, sql)
        print ("Number of affected rows: ", ibm_db.num_rows(stmt))   
        return f_assignment()
    

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == "POST":
        usn = request.form['usn']
        name = request.form['name']
        branch = request.form['branch']
        semester = request.form['semester']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['pwd']      
        
        
        #inp=[name,email,contact,address,role,branch,password]
        insertdb(conn,usn,name,branch,semester,email,phone,password)
        return render_template('login.html')
        
@app.route('/f_register', methods=['POST','GET']) 
def f_register():
    if request.method == "POST":
        name = request.form['name']
        designation = request.form['designation']
        branch = request.form['branch']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['pwd']      
        
        #inp=[name,email,contact,address,role,branch,password]
        insertfaculty(conn,name,designation,branch,email,phone,password)
        return render_template('login.html')

@app.route('/admin_register', methods=['POST','GET'])
def admin_register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['pwd']      

        sql= "insert into admin values('{}','{}','{}','{}')".format(name, email, phone, password)
        stmt = ibm_db.exec_immediate(conn, sql)
        print ("Number of affected rows: ", ibm_db.num_rows(stmt))   
        return render_template('login.html')

@app.route('/userprofile', methods=['POST','GET'])
def userprofile():
    email=session['register']
    sql= "select * from STUDENT where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    userdetails = ibm_db.fetch_both(stmt)
    return render_template('userprofile.html',usn=userdetails["USN"],name=userdetails["NAME"],branch=userdetails["BRANCH"],semester=userdetails["SEMESTER"],email= userdetails["EMAIL"],phone=userdetails["PHONE"],role="Student")

@app.route('/facultyprofile', methods=['POST','GET'])
def facultyprofile():
    email=session['register']
    sql= "select * from FACULTY where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    userdetails = ibm_db.fetch_both(stmt)
    return render_template('facultyprofile.html',name=userdetails["NAME"],designation=userdetails["DESIGNATION"],branch=userdetails["BRANCH"],email= userdetails["EMAIL"],phone=userdetails["PHONE"],role="Faculty")

@app.route('/adminprofile', methods=['POST', 'GET'])
def adminprofile():
    email=session['register']
    sql= "select * from admin where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    userdetails = ibm_db.fetch_both(stmt)
    return render_template('adminprofile.html', data=userdetails, role="Admin")

@app.route('/f_assignment', methods=['POST','GET'])
def f_assignment():
    email=session['register']
    sql= "select * from FACULTY where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    userdetails = ibm_db.fetch_both(stmt)
    
    sql="select max(ASSN_NO) from assignment"
    stmt=ibm_db.exec_immediate(conn, sql)
    assigndetails = ibm_db.fetch_both(stmt)
    
    if assigndetails[0] == None:
        assign_no = 1
    else:
        assign_no = int(assigndetails[0]) + 1
 
    assigndetails=()    
    sql="select * from assignment where faculty_id='{}'".format(email)
    stmt=ibm_db.exec_immediate(conn, sql)
    tuples = ibm_db.fetch_tuple(stmt) 
    assigndetails = assigndetails+(tuples,)
    while tuples != False:
        assigndetails = assigndetails + (tuples:=ibm_db.fetch_tuple(stmt),)
    assigndetails=assigndetails[:-1]
    print(assigndetails)
    
    subdetails=()
    sql="select a.assn_no, count(*) from assignment a, submission s where faculty_id='{}' and a.assn_no=s.assn_no group by a.assn_no".format(email)
    stmt=ibm_db.exec_immediate(conn, sql)
    tuples = ibm_db.fetch_tuple(stmt) 
    subdetails = subdetails+(tuples,)
    while tuples != False:
        subdetails = subdetails + (tuples:=ibm_db.fetch_tuple(stmt),)
    subdetails=subdetails[:-1]
    print(subdetails)
    
    return render_template('facultyassignment.html', name=userdetails["NAME"], role="Faculty", assign_no=assign_no, email=email, data=assigndetails, subdata=subdetails)

@app.route('/s_assignment', methods=['POST','GET'])
def s_assignment():
    email=session['register']
    sql= "select * from STUDENT where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    userdetails = ibm_db.fetch_both(stmt)
    
    assigndetails=()    
    sql="select * from assignment a, faculty f, student s where f.branch=s.branch and f.email=a.faculty_id and s.email='{}'".format(email)
    stmt=ibm_db.exec_immediate(conn, sql)
    tuples = ibm_db.fetch_tuple(stmt) 
    assigndetails = assigndetails+(tuples,)
    while tuples != False:
        assigndetails = assigndetails + (tuples:=ibm_db.fetch_tuple(stmt),)    
    assigndetails=assigndetails[:-1]    
    
    
    subdetails=()
    sql="select assn_no from submission where student_id='{}'".format(email)
    stmt=ibm_db.exec_immediate(conn, sql)
    sub_tuples = ibm_db.fetch_tuple(stmt)
    subdetails = subdetails+(sub_tuples,)
    while sub_tuples != False:
        subdetails = subdetails + (sub_tuples:=ibm_db.fetch_tuple(stmt),)
    subdetails=subdetails[:-1]
    print(subdetails)
    
    return render_template('studentassignment.html', name=userdetails["NAME"], role="Student", data=assigndetails, subdata=subdetails)

@app.route('/submitassignment', methods=['POST','GET'])
def submitassignment():
    if request.method == "POST":
        
        email = session['register'] 
        assn_no = request.form['assn_no']        
        file = request.files['filename']        
        sub_date = date.today()   
        filename = file.filename
        print(filename)
        sql="insert into submission(student_id, assn_no, sub_date, filename) values('{}',{},'{}','{}')".format(email, assn_no, sub_date, filename)
        stmt=ibm_db.exec_immediate(conn, sql)   
        print ("Number of affected rows: ", ibm_db.num_rows(stmt))   
        
        basepath = os.path.dirname(__file__)
        #filepath = os.path.join(basepath,'uploads',file.filename)
        filepath = os.path.join(basepath,'uploads',email+'_'+assn_no+'.pdf')
        file.save(filepath)
        
        
        COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
        COS_API_KEY_ID = "zZVIS50s1eKNy11NqJfBlmNvUcz4-SZ2sGyUH4Bp2vXK"
        COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/5d28c261943a461a91eeb0dfc6530ff2:fb22c7db-125b-468e-90e9-2f0eec95ab09::"
        cos = ibm_boto3.resource("s3", ibm_api_key_id=COS_API_KEY_ID, ibm_service_instance_id=COS_INSTANCE_CRN, config=Config(signature_version="oauth"), endpoint_url=COS_ENDPOINT)
        print(cos)
        cos.meta.client.upload_file(Filename=filepath, Bucket='smcadbucket', Key=email+'_'+assn_no+'.pdf')
        
        return s_assignment()
 
@app.route('/download', methods=['POST','GET'])
def download():
    file=request.form['file']
    print(file)
    COS_ENDPOINT = "https://s3.jp-tok.cloud-object-storage.appdomain.cloud"
    COS_API_KEY_ID = "zZVIS50s1eKNy11NqJfBlmNvUcz4-SZ2sGyUH4Bp2vXK"
    COS_INSTANCE_CRN = "crn:v1:bluemix:public:cloud-object-storage:global:a/5d28c261943a461a91eeb0dfc6530ff2:fb22c7db-125b-468e-90e9-2f0eec95ab09::"
    cos = ibm_boto3.resource("s3", ibm_api_key_id=COS_API_KEY_ID, ibm_service_instance_id=COS_INSTANCE_CRN, config=Config(signature_version="oauth"), endpoint_url=COS_ENDPOINT)
    print(cos)
    cos.meta.client.download_file(Filename=file, Bucket='smcadbucket', Key=file)
    return viewsubmission()
    
@app.route('/viewsubmission', methods=['POST','GET'])
def viewsubmission():
    email = session['register']
    print("Success")
    assn_no = request.form['assn_no']
   
    sql= "select name from faculty where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    userdetails = ibm_db.fetch_both(stmt)
    
    subdetails=()
    sql="select * from assignment a, submission s, student st where s.assn_no=a.assn_no and st.email = s.student_id and a.faculty_id='{}' and s.assn_no={}".format(email, assn_no)
    stmt=ibm_db.exec_immediate(conn, sql)   
    sub_tuples = ibm_db.fetch_tuple(stmt)
    subdetails = subdetails+(sub_tuples,)
    while sub_tuples != False:
        subdetails = subdetails + (sub_tuples:=ibm_db.fetch_tuple(stmt),)
    subdetails=subdetails[:-1]
    print(subdetails)
    return render_template('viewsubmission.html', name=userdetails["NAME"], role="Faculty", subdata=subdetails)
    
@app.route('/evaluate', methods=['POST','GET'])
def evaluate():
    student_id = request.form['student_id']
    assn_no = request.form['assn_no']
    marks = request.form['marks']
    sql="update submission set marks={} where assn_no={} and student_id='{}'".format(marks, assn_no, student_id)
    stmt=ibm_db.exec_immediate(conn, sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))    
    return viewsubmission()
    
@app.route('/facultylist', methods=['POST', 'GET'])
def facultylist():
    email=session['register']
    sql= "select * from admin where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    admindetails = ibm_db.fetch_both(stmt)
    
    details=()
    sql="select * from faculty"
    stmt=ibm_db.exec_immediate(conn, sql)
    tuples = ibm_db.fetch_tuple(stmt)
    details = details+(tuples,)
    while tuples != False:
        details = details + (tuples:=ibm_db.fetch_tuple(stmt),)
    details=details[:-1]
    print(details)
    return render_template('adminfacultylist.html', data=details, name=admindetails["NAME"], role="Admin")
    
@app.route('/studentlist', methods=['POST', 'GET'])
def studentlist():
    email=session['register']
    sql= "select * from admin where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    admindetails = ibm_db.fetch_both(stmt)
    
    details=()
    sql="select * from student"
    stmt=ibm_db.exec_immediate(conn, sql)
    tuples = ibm_db.fetch_tuple(stmt)
    details = details+(tuples,)
    while tuples != False:
        details = details + (tuples:=ibm_db.fetch_tuple(stmt),)
    details=details[:-1]
    print(details)
    return render_template('adminstudentlist.html', data=details, name=admindetails["NAME"], role="Admin")


@app.route('/assignmentlist', methods=['POST', 'GET'])
def assignmentlist():
    email=session['register']
    sql= "select * from admin where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    admindetails = ibm_db.fetch_both(stmt)
        
    assigndetails=()    
    sql="select * from assignment a, faculty f where a.faculty_id=f.email"
    stmt=ibm_db.exec_immediate(conn, sql)
    tuples = ibm_db.fetch_tuple(stmt) 
    assigndetails = assigndetails+(tuples,)
    while tuples != False:
        assigndetails = assigndetails + (tuples:=ibm_db.fetch_tuple(stmt),)
    assigndetails=assigndetails[:-1]
    print(assigndetails)
    
    subdetails=()
    sql="select a.assn_no, count(*) from assignment a, submission s where a.assn_no=s.assn_no group by a.assn_no"
    stmt=ibm_db.exec_immediate(conn, sql)
    tuples = ibm_db.fetch_tuple(stmt) 
    subdetails = subdetails+(tuples,)
    while tuples != False:
        subdetails = subdetails + (tuples:=ibm_db.fetch_tuple(stmt),)
    subdetails=subdetails[:-1]
    print(subdetails)
    
    return render_template('adminassnlist.html', name=admindetails["NAME"], role="Admin", data=assigndetails, subdata=subdetails)
    
@app.route('/adminsublist', methods=['POST','GET'])
def adminsublist():
    assn_no = request.form['assn_no']
    email=session['register']
    
    sql= "select * from admin where email='{}'".format(email)
    stmt = ibm_db.exec_immediate(conn, sql)
    admindetails = ibm_db.fetch_both(stmt)
       
    subdetails=()
    sql="select * from assignment a, submission s, student st where s.assn_no=a.assn_no and st.email = s.student_id and s.assn_no={}".format(assn_no)
    stmt=ibm_db.exec_immediate(conn, sql)   
    sub_tuples = ibm_db.fetch_tuple(stmt)
    subdetails = subdetails+(sub_tuples,)
    while sub_tuples != False:
        subdetails = subdetails + (sub_tuples:=ibm_db.fetch_tuple(stmt),)
    subdetails=subdetails[:-1]
    print(subdetails)
    return render_template('adminsublist.html', name=admindetails["NAME"], role="Admin", subdata=subdetails)
    
    
@app.route('/loginpage', methods=['GET','POST'])
def loginpage():
    return render_template('login.html')
    
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == "POST":
        role = request.form['role']
        email = request.form['email']
        password = request.form['pwd']
        
        if role == "student":
            sql= "select * from STUDENT where email='{}' and password='{}'".format(email,password)
            stmt = ibm_db.exec_immediate(conn, sql)
            userdetails = ibm_db.fetch_both(stmt)
            print(userdetails)
            if userdetails:
                session['register']=userdetails["EMAIL"]
                return render_template('userprofile.html',usn=userdetails["USN"],name=userdetails["NAME"],branch=userdetails["BRANCH"],semester=userdetails["SEMESTER"],email= userdetails["EMAIL"],phone=userdetails["PHONE"],role="Student")
            else:
                msg = "Incorrect Email id or Password"
                return render_template("login.html", msg=msg)
            return render_template('login.html')
        
        if role == "faculty":
            sql= "select * from FACULTY where email='{}' and password='{}'".format(email,password)
            stmt = ibm_db.exec_immediate(conn, sql)
            userdetails = ibm_db.fetch_both(stmt)
            print(userdetails)
            if userdetails:
                session['register']=userdetails["EMAIL"]
                return render_template('facultyprofile.html',name=userdetails["NAME"],designation=userdetails["DESIGNATION"],branch=userdetails["BRANCH"],email= userdetails["EMAIL"],phone=userdetails["PHONE"],role="Faculty")
            else:
                msg = "Incorrect Email id or Password"
                return render_template("login.html", msg=msg)
            return render_template('login.html')

        if role == "admin":
            sql="select * from admin where email='{}' and password='{}'".format(email, password)
            stmt = ibm_db.exec_immediate(conn, sql)
            userdetails = ibm_db.fetch_both(stmt)
            print(userdetails)
            if userdetails:
                session['register']=userdetails["EMAIL"]
                return render_template('adminprofile.html', data=userdetails, role="Admin")
            else:
                msg = "Incorrect Email id or Password"
                return render_template("login.html", msg=msg)
            return render_template('login.html')

if __name__ =='__main__':
    app.run( debug =False)
#Keep debug=False to check output in terminal