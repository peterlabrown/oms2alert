import yaml
import mysql.connector
import mailparser
import datetime
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

# Get configuration information
with open("config.yml", 'r') as ymlfile:
  cfg = yaml.load(ymlfile)

# create message object instance
msg = MIMEMultipart()

password = cfg['email']['sender_password']
msg['From'] = cfg['email']['sender']
msg['To'] = cfg['email']['recipient']
msg['Subject'] = cfg['email']['subject']

mydb = mysql.connector.connect(
  host=cfg['mysql']['host'],
  user=cfg['mysql']['dbuser'],
  passwd=cfg['mysql']['dbuser_password'],
  database=cfg['mysql']['database']
)

dbcursor = mydb.cursor()
insertsql = "INSERT INTO `alertstate` (`datetime`, `computer`, `confmic`, `confspeaker`, `defaultmic`, `camera`, `display`, `motion`, `hdmi`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
auditsql = "INSERT INTO `alerts` (`datetime`, `computer`, `confmic`, `confspeaker`, `defaultmic`, `camera`, `display`, `motion`, `hdmi`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
updatesql = "UPDATE alertstate SET `datetime` = %s, `computer` = %s, `confmic` = %s, `confspeaker` = %s, `defaultmic` = %s, `camera` = %s, `display` = %s, `motion` = %s, `hdmi` = %s WHERE computer LIKE %s"
selectsql = "SELECT * FROM `alertstate` WHERE `computer` LIKE %s ORDER BY `datetime` DESC LIMIT 1"
getcompssql = "SELECT * FROM `alertstate`"
columns = ("Time Stamp", "Computer", "Conference Mic", "Conference Speaker", "Default Mic", "Camera", "Display", "Motion Sensor", "HDMI Ingres")
insertlist = []
emailbody = []
newentry = 0
message = ""

if os.path.exists("/home/peter/dfsioms/omshwfile.txt"):
  omsfile = open("/home/peter/dfsioms/omshwfile.txt", "r")
  for line in omsfile:
    field = line.split()
    if len(field) > 1:
      if field[0] == "TimeGenerated":
        subfield = field[1].split("T")
        insertlist.append(subfield[0] + " " + subfield[1])
      if field[0] == "Computer":
        computertup = (field[1],) # MYSQL Connector needs a tupple
        computer = field[1] # Need a string to constuct the insert list
        dbcursor.execute(selectsql, computertup)
        selectlist = dbcursor.fetchone()
        if dbcursor.rowcount < 1:
          newentry = 1
          selectlist = [0,computertup, 0, 0, 0, 0, 0, 0, 0]
        insertlist.append(computer)
      if field[0] == "RenderedDescription":
        j = 2
        for i in [5, 10, 15, 19, 26, 31, 36]:
          if field[i] == "Healthy.":
            if selectlist[j] != 0:
              message = message + columns[j] + " on " +insertlist[1] + " is working again\n"
            insertlist.append(0) #Healthy
          else:
            if selectlist[j] != 1:
              message = message + columns[j] + " on " +insertlist[1] + " has stopped working\n"
            insertlist.append(1) #Unhealthy
          j = j + 1
  		
  # After we get RenderedDescription, we have all the data for the row
        val = tuple(insertlist)
        dbcursor.execute(auditsql, val)
        if newentry == 0:
          insertlist.append(computer) # add computer for the update
          val = tuple(insertlist)
          dbcursor.execute(updatesql, val)
        else:
          dbcursor.execute(insertsql, val)
        insertlist.clear() # reset the insertlist
        newentry = 0 # reset newentry
        mydb.commit()
#else:
#  print("/home/peter/dfsioms/omshwfile.txt does not exist")

# Reset the alert state for any computers we havent heard anything about for 3 hours
ts = datetime.datetime.utcnow()
dbcursor.execute(getcompssql)
selectlist = dbcursor.fetchall()
if dbcursor.rowcount < 1:
  print("Empty data set")
for row in selectlist:
  val = (ts, row[1], 0, 0, 0, 0, 0, 0, 0, row[1])
  if row[0] < datetime.datetime.utcnow() - datetime.timedelta(hours=2): # Only if the timestamp is more than 2 hours old
    if row[2] + row[3] + row[4] + row[5] + row[6] + row[7] + row[8] > 0: # Only alert good if current state bad
      message = message + "Everything on " + row[1] + " appears to be working again (no news is good news, right?)\n"
      dbcursor.execute(updatesql, val)
      mydb.commit()

# add in the message body
msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP('dfsi.itchi.consulting', 25)
server.starttls()
server.login(msg['From'], "Troubleon2!")

if len(message) > 0:
  server.sendmail(msg['From'], msg['To'].split(","), msg.as_string())
server.quit()

if os.path.exists("/home/peter/dfsioms/omshwfile.txt"):
  os.remove("/home/peter/dfsioms/omshwfile.txt")
