import time
import sys
import math
from MyConnect import arm_drone
from dronekit import VehicleMode, LocationGlobalRelative
import Constants

#setting the takeoff
def takeoff(vehicle):
	while True:
		try:
			#TODO: verify minimum safe altitude
			altitude_input = raw_input("type a takeoff altitude[m]: ")
			aTargetAltitude = float(altitude_input)
			break
		except ValueError:
			print("That's not a number!")
	#arming drone		
	arm_drone(vehicle)
	print "takeoff to %f" % aTargetAltitude
	vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude
	# Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
	#  after Vehicle.simple_takeoff will execute immediately).
	while True:
	    print " Altitude: ", vehicle.location.global_relative_frame.alt
	    #Break and return from function just below target altitude.
	    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*(1 - Constants.MAX_DIFFERENCE_ALTITUDE):
		print "Reached target altitude"
		print "current altitude: %s" % vehicle.location.global_relative_frame.alt
		break
	    time.sleep(1)

def landing(vehicle):
	print "initiating landing"
	vehicle.mode = VehicleMode("LAND")
	print " Altitude: ", vehicle.location.global_relative_frame.alt
	while vehicle.location.global_relative_frame.alt > Constants.MAX_DIFFERENCE_ALTITUDE:
		print " Altitude: ", vehicle.location.global_relative_frame.alt
		time.sleep(1)
	print "landing complete"	
