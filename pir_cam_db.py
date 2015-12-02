import RPi.GPIO as GPIO 
import time 
import MySQLdb
import datetime
import picamera

def insertdb (type, date):
	db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                     passwd="****", # your password
                     db="raspberry") # name of the data base
	with db:
# you must create a Cursor object. It will let
#  you execute all the queries you need
		cur = db.cursor()
# Use all the SQL you like
			
		cur.execute("insert into motion (Type, Date) values (%s,%s)",(type,date)) 

GPIO.setmode(GPIO.BCM) 
GPIO_PIR = 4 

print "PIR Module Test (CTRL-C to exit)" 

GPIO.setup(GPIO_PIR,GPIO.IN) # Echo 
Current_State = 0 
Previous_State = 0 
camera = picamera.PiCamera()
camera.resolution = (1920, 1080)

try:
  print "Waiting for PIR to settle ..."
  while GPIO.input(GPIO_PIR)==1:
    Current_State = 0
  print " Ready"
  while True :
   
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
   
    if Current_State==1 and Previous_State==0:
      fulltime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
      parttime = fulltime[11:]
      camTime = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
      # PIR is triggered
      print " Motion detected at: ", fulltime
      print " Inserting to db..."
      insertdb('Motion at',fulltime)
      # Record previous state
      print " Capturing... "
      camera.capture('/home/pi/scripts/img/motion_%s.jpg' % (camTime))
      print " OK "
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      print " Ready"
      Previous_State=0
      
    # Wait for 10 milliseconds
    time.sleep(0.01)
      
except KeyboardInterrupt:
  print " Quit"
  # Reset GPIO settings
  GPIO.cleanup()
