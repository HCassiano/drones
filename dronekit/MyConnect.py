import time
import sys
import math
from dronekit import connect, VehicleMode
import Constants

def my_connect(connection_string):
	# Connect to the Vehicle.
	#Use a try/except block
	print("Connecting to vehicle on: %s" % (connection_string))
	vehicle = connect(connection_string, wait_ready=True)

	# Get some vehicle attributes (state)
	print "Get some vehicle attribute values:"
	print " GPS: %s" % vehicle.gps_0
	print " Battery: %s" % vehicle.battery
	print " Last Heartbeat: %s" % vehicle.last_heartbeat
	print " Is Armable?: %s" % vehicle.is_armable
	print " System status: %s" % vehicle.system_status.state
	print " Mode: %s" % vehicle.mode.name    # settable
	print " Is Armed? %s" % vehicle.armed
	return vehicle

def arm_drone(vehicle):
	#setting for GUIDED mode
	while(True):
		if vehicle.is_armable == True:
			try:
				vehicle.mode = VehicleMode("GUIDED")
				print "Vehicle set to guided"
			except:
				print "error in setting vehicle to guided"
			break
		else:
			print "waiting for drone to be armable"
			time.sleep(1) #wait for 1 second before pooling

	#setting the drone as ARMED
	arming_iterations = 0
	vehicle.armed = True
	while(True):
		#pooling:
		if vehicle.armed == True:
			print "vehicle is armed"
			break
		else:
			print "vehicle not armed, trying again"
			arming_iterations = arming_iterations + 1
			time.sleep(1) #wait for 1 second before rearming
		if arming_iterations == Constants.MAX_ARMING_ITERATIONS: #5 seconds/arming tries
			print "arming failed, stopping execution"
			sys.exit(0) #change as necessary
