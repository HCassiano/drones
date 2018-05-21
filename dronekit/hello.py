#connection_string = sitl.connection_string()
connection_string = "tcp:127.0.0.1:5760"

# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import sys
import math
import GotoMeters
from MyConnect import my_connect
import LandingTakeoff
import Constants

vehicle = my_connect(connection_string)

isDroneOnAir = False
while True: #command loop
	try:
		user_input = int(raw_input("type 1 for takeoff, 2 to specify a destination, 3 for landing, 4 for exit: \n"))
		#user_input = int(raw_user_input)
	except ValueError:
		print("That's not a valid command!")
		continue
	#verifiy command switch
	#fail cases	
	if (user_input == 1 and isDroneOnAir == True):
		print("Drone has already taken off!")
	elif (user_input == 2 and isDroneOnAir == False):
		print("Drone must takeoff before moving!")
	elif (user_input == 3 and isDroneOnAir == False):
		print("Drone must takeoff before landing!")
	elif (user_input == 4 and isDroneOnAir == True):
		print("Drone must land before exiting!")
	#acceptable commands
	elif (user_input == 1):
		LandingTakeoff.takeoff(vehicle)	
		isDroneOnAir = True
	elif (user_input == 2):
		GotoMeters.my_goto(vehicle)	
	elif (user_input == 3):
		LandingTakeoff.takeoff(vehicle)
		isDroneOnAir = False
	elif (user_input == 4):
		print("exiting...")
		break
	else:
		print("That's not a valid command!")		

# Close vehicle object before exiting script
vehicle.close()
print("Completed")

