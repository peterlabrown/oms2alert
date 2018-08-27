import datetime
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="peter",
  passwd="ay2M7lE5YKqZ2kAb",
  database="dfsioms"
)
mycursor = mydb.cursor()
insertsql = "INSERT INTO `alerts` (`datetime`, `computer`, `confmic`, `confspeaker`, `defaultmic`, `camera`, `display`, `motion`, `hdmi`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
selectsql = "SELECT DISTINCT `computer`, MAX(`datetime`) FROM `alerts` GROUP BY `computer`"
ts = datetime.datetime.now()

mycursor.execute(selectsql)
selectlist = mycursor.fetchall()
if mycursor.rowcount == 0:
  print("Empty data set")
for row in selectlist:
  computer = row[0]
  print(computer)
  val = (ts, computer, 0, 0, 0, 0, 0, 0, 0)
#  mycursor.execute(insertsql, val)
#mydb.commit()