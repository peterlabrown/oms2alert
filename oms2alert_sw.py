import mysql.connector
import datetime
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="peter",
  passwd="ay2M7lE5YKqZ2kAb",
  database="dfsioms"
)
dbcursor = mydb.cursor()
insertsql = "INSERT INTO `swalertstate` (`datetime`, `computer`, `network`, `exchange`, `signin`) VALUES (%s, %s, %s, %s, %s)"
auditsql = "INSERT INTO `swalerts` (`datetime`, `computer`, `network`, `exchange`, `signin`) VALUES (%s, %s, %s, %s, %s)"
updatesql = "UPDATE swalertstate SET `datetime` = %s, `computer` = %s, `network` = %s, `exchange` = %s, `signin` = %s WHERE computer LIKE %s"
selectsql = "SELECT * FROM `swalertstate` WHERE `computer` LIKE %s"
getcompssql = "SELECT `datetime`, `computer` FROM `swalertstate`"
columns = ("Time Stamp", "Computer", "Network", "Exchange", "SignIn")
insertlist = []
emailbody = []
newentry = 0

if os.path.exists("/home/peter/dfsioms/omsswfile.txt"):
  omsfile = open("/home/peter/dfsioms/omsswfile.txt", "r")
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
          selectlist = [0,computertup, 0, 0, 0]
        insertlist.append(computer)
      if field[0] == "RenderedDescription":
        if len(field) == 15:
          x = len(field)
          j = 2
          for i in [4, 8, 11]:
            if field[i] == "Healthy.":
              if selectlist[j] != 0:
                print(columns[j], " on ", insertlist[1], " is working again")
              insertlist.append(0) #Healthy
            else:
              if selectlist[j] != 1:
                print(columns[j], " on ", insertlist[1], " has stopped working")
              insertlist.append(1) #Unhealthy
            j = j + 1
        else:
          insertlist.clear() # reset the insertlist
          newentry = 0 # reset newentry
          continue

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

#
## Reset the alert state for any computers we havent heard anything about for 3 hours
ts = datetime.datetime.utcnow()
dbcursor.execute(getcompssql)
selectlist = dbcursor.fetchall()
if dbcursor.rowcount < 1:
  print("Empty data set")
for row in selectlist:
  val = (ts, row[1], 0, 0, 0, row[1])
  if row[0] < datetime.datetime.utcnow() - datetime.timedelta(hours=3):
#    print("Everything on ", row[1], " appears to be working again (no news is good news, right?)")
    dbcursor.execute(updatesql, val)
mydb.commit()

if os.path.exists("/home/peter/dfsioms/omsswfile.txt"):
  os.remove("/home/peter/dfsioms/omsswfile.txt")
