#Creates .txt doc
#This file makes the document that Mr. Feid needs to print. It should have everything that Mr. Feid wants to file.
#Add this code to the correct block and
#Sub the variables for the actual ones
#fh = filehandler
from datetime import date

today = date.today()

#proposed variables:
"""
Date
ID
customer
  
Issue:


Ask someone in auto about how the labs are made. I can make a template off of that



Repair
"""
#var should be set in app.py
def setAF(var):
    AF = var

AF = 1
setAF()
#boolean for accepted print file or finished print file
if AF == 1:
    fh = open('accepted.txt', 'w')
    fh.write("Today's date:")
    #For some reason the todays date doesnt work. Also, ill just add this to the github since it shows hot to make a txt file. Its not that hard
    fh.write(today)
    fh.close()
if AF == 2:
    fh = open('rejected.txt', 'w')
    fh.write("Today's date:")
    fh.write(today)
    fh.close()
