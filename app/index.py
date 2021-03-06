from flask import Blueprint, render_template, session
from app.database import query_db
import app.toolkit as EZ
import app
from app import validation
from app import toolkit
from flask import request
from flask import flash
#from app.toolkit import setRepairState
#from app.toolkit import getRepairState
bp = Blueprint("index", __name__)
from app.toolkit import *
from flask_mail import Mail, Message
from app import create_app
import os
from app import create_app

app = create_app()
app.config['SECRET_KEY'] = 'superSecretGlobalKey'
#Config SMTP with App
with app.app_context():
    mail = Mail(app)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com' #This sends requst to google
    app.config['MAIL_PORT'] = 465 #This is required for the server
    app.config['MAIL_USERNAME'] = 'nchs.autoshop@gmail.com' #Associates sender address
    app.config['MAIL_PASSWORD'] = 'nchsautowebsite' #Validates sender with password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    print("See")
# PATHS ------------------------------------------------------------------------------------------------------

#Way to fake-instantiate the database
@bp.route("/functionTest", methods=["GET"])
def functiontest():
    # Something in order troubleshoot: literally calling just about everything in the file. (May have to re-instantiate the database
    # from dummyTester.py because no vin and things yet.
    entries = query_db("""
        SELECT customers.customerName, customers.customerEmail, vehicles.make, vehicles.model, repairs.repairType, repairs.repairId
        FROM ((vehicles INNER JOIN customers ON vehicles.customerID = customers.customerID)
        INNER JOIN repairs ON vehicles.vehicleId = repairs.vehicleID)""")
    
    getId = query_db("SELECT vehicleId FROM vehicles ORDER BY vehicleId DESC", one = True)
    print (getId)


       # for entry in entries:
        #This is where we can put the tests to make
        #sure that Sean's things actually work.
    #    print ("Repair Type:", entry["repairType"])
    #    print ("Repair ID:", entry["repairId"])
    #EZ.test()
   

  
        
    
    #You have to grab the repairIds again because they've changed.
    myIds = EZ.getRepairIds()
    EZ.test()
   
    print ("BEFORE:")
    myIds = EZ.getRepairIds()
    #Getting repair Types with the getter. 
    for repairId in myIds:
        print (repairId)
        print("Repair ID:",repairId, "\nRepair Type:",EZ.getRepairType(repairId))

    print("AFTTER:")
    return render_template("login.html")

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login.html')
def login():
    return render_template('login.html')


@bp.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form.to_dict()
        ok = "True"

        if ok == "True":
            ##if required fields arent filled out
            if validation.hasData(result['customerName']) == 0:
                print("required name")
                flash("required name")

                ok = "False"

            if validation.hasData(result['customerEmail']) == 0:
                print("required email")
                flash("required email")
                ok = "False"

            if validation.hasData(result['repairType']) == 0:
                print("required fields aint filled out")
                flash("required repairType")
                ok = "False"

            ##require repairDescription if repair type is other
            if result['repairType'] == "other":
                if validation.hasData(result['repairDescription']) == 0:
                    print("require repair description")
                    flash("required email")
                    ok = "False"

            if validation.hasData(result['vin']) == 1:
                ## if vin number is entered incorrerctly
                if validation.vinNumber(result['vin']) == 0:
                    flash("vin number is invalid")
                    ok = "False"

            ##check make
            if validation.hasData(result['make']) == 0:
                flash("Vehicle make is required")
                ok = "False"
            if validation.hasData(result['model']) == 0:
                flash("Vehicle model is required")
                ok = "False"
            if validation.hasData(result['year']) == 0:
                flash("Vehicle year is required")
                ok = "False"

                ##check if the email is correct
            if validation.emailChecker(result['customerEmail']) == "False":
                flash("Email is invalid")
                print("this email is WRONG")

            if ok == "True":
                toolkit.publish(result)
                render_template("success.html")

    return render_template("login.html")

# # test email
# @bp.route("/test_sendEmail")
# def test_sendEmail():
#     #email template can be found at app/templates/testEmail.html
#     sendEmail("This is a test email!", render_template("testEmail.html"), "spkudrna@gmail.com")
#     return("email test succefully fired, check target inbox.")

#Change the template directory for render_template
template_dir = os.path.abspath("./app/templates")

#Basically what you need to do is add the response.html as an actual route
@bp.route('/response', methods = ['GET','POST'])
def response():
    if request.method == "POST":
        req = request.form
        ccr = "y" + req.get("CCR")
        date = "e" + req.get('date')
        desc = "s" + req.get('desc')
        return sent(ccr, date, desc)
    return render_template("response.html")

# MADD RESPONSE FUNCTION TO INDEX AND SEE IF IT WORKS FROM THERE
@bp.route("/sent")
def sent(ccr, date, desc):
    msg = Message("y i k e s",
                  sender = "nchs.autoshop@gmail.com",
                  recipients=["rsziegler@stu.naperville203.org"])
    msg.body = "\n Do not respond to this email \n " + ccr + "When can you bring your car in? (Please make it within a week):" + date + "\nAlso:" + desc
    mail.send(msg)  # something wrong here?
    return render_template("response.html")

# admin console routes
@bp.route("/admin")
def adminConsole():
    return(render_template("console.html", compiledData=toolkit.compileRequestData()))

# for the email stuff, i think we should return a function that returns a render_template with the email page (like in line 154, but with email)
@bp.route("/admin/L/<repairID>", methods=['GET','POST'])
def sinistra(repairID):
    if (getRepairAccepted(repairID) == 0 and getRepairRejected(repairID) == 0 and getRepairCompleted(repairID) == 0): # pending
        setRepairAccepted(repairID, 1)
        setRepairCompleted(repairID, 0)
        setRepairRejected(repairID, 0)
    elif (getRepairAccepted(repairID) == 1 and getRepairRejected(repairID) == 0 and getRepairCompleted(repairID) == 0): # in progress
        setRepairAccepted(repairID, 0)
        setRepairCompleted(repairID, 1)
        setRepairRejected(repairID, 0)
    elif (getRepairAccepted(repairID) == 0 and getRepairRejected(repairID) == 0 and getRepairCompleted(repairID) == 1):  # completed
        setRepairAccepted(repairID, 0)
        setRepairCompleted(repairID, 0)
        setRepairRejected(repairID, 0)
    elif (getRepairAccepted(repairID) == 0 and getRepairRejected(repairID) == 1 and getRepairCompleted(repairID) == 0): # rejected
        setRepairAccepted(repairID, 0)
        setRepairCompleted(repairID, 0)
        setRepairRejected(repairID, 0)
    return adminConsole()

@bp.route("/admin/R/<repairID>", methods=['GET','POST'])
def destra(repairID):
    if (getRepairAccepted(repairID) == 0 and getRepairRejected(repairID) == 0 and getRepairCompleted(repairID) == 0): # pending
        setRepairAccepted(repairID, 0)
        setRepairCompleted(repairID, 0)
        setRepairRejected(repairID, 1)
    elif (getRepairAccepted(repairID) == 1 and getRepairRejected(repairID) == 0 and getRepairCompleted(repairID) == 0): # in progress
        # print
        print("print")
    elif (getRepairAccepted(repairID) == 0 and getRepairRejected(repairID) == 0 and getRepairCompleted(repairID) == 1):  # completed
        # purge
        setRepairAccepted(repairID, 1)
        setRepairCompleted(repairID, 1)
        setRepairRejected(repairID, 1)
    elif (getRepairAccepted(repairID) == 0 and getRepairRejected(repairID) == 1 and getRepairCompleted(repairID) == 0): # rejected
        # purge
        setRepairAccepted(repairID, 1)
        setRepairCompleted(repairID, 1)
        setRepairRejected(repairID, 1)
    return adminConsole()

# end admin paths

#Route to purge the database... smart idea
@bp.route("/purge/database/<secretKey>")
def seanThinksThisIsInsaneAndHeIsCorrect(secretKey):
    if secretKey == app.config['SECRET_KEY']:
        toolkit.BIG_RED_BUTTON()
        return("bye bye...")
    else:
        return("nope.")