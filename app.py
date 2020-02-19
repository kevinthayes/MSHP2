import os
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
#from flask_mail import Mail, Message
from app import create_app
from app import validation
from app import toolkit

#This NEEDS to Stay at TOP of This File. If You Move it, I Will be VERY MAD AT YOU! Be Warned...
app = create_app()
app.config['SECRET_KEY'] = 'superSecretGlobalKey'




#Change the template directory for render_template
template_dir = os.path.abspath("./app/templates")


#Config SMTP with App
#with app.app_context():
    #mail = Mail(app)
    #app.config['MAIL_SERVER'] = 'smtp.gmail.com' #This sends requst to google
    #app.config['MAIL_PORT'] = 465 #This is required for the server
    #app.config['MAIL_USERNAME'] = 'NCHS.autoshop@gmail.com' #Associates sender address
    #app.config['MAIL_PASSWORD'] = 'nchsautowebsite' #Validates sender with password
    #app.config['MAIL_USE_TLS'] = False
    #app.config['MAIL_USE_SSL'] = True
    #mail = Mail(app)
    #print("See")

#This NEEDS to Stay at BOTTOM of This File. If You Move it, I Will be VERY MAD AT YOU! Be Warned...
if __name__ == "__main__":
    app.run(debug=True) #this should probably be False in a productoin environent...
