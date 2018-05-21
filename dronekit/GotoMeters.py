#notes:
#fi -> lon
#lambda -> lat
import time
import sys
import math
from MyConnect import arm_drone
from dronekit import VehicleMode, LocationGlobalRelative
import Constants

def calculate_distance_in_m(fi_initial, fi_final, lambda_initial, lambda_final):
	delta_lambda = 	lambda_final - lambda_initial
	delta_fi = fi_final - fi_initial
	x = delta_fi * Constants.ARC
	y = delta_lambda * Constants.ARC * math.cos(fi_final) 	
	return (x,y)

def calculate_degrees_with_distance(fi_initial, lambda_initial, x, y):
	fi_final = (y/Constants.ARC) + fi_initial
	lambda_final = (x/(Constants.ARC*math.cos(fi_final))) + lambda_initial
	return (fi_final,lambda_final)
	 
def my_goto(vehicle):
	#set movement in north and east
	while True:
		try:
			x_input = raw_input("type a distance in north[m]: ")
	   		x_objective = float(x_input)
			y_input = raw_input("type a distance in east[m]: ")
			y_objective = float(y_input)
			z_input = raw_input("type a altitude in z[m]: ")
			z_objective = float(z_input)
			v_input = raw_input("type a speed in v[m/s]: ")
			v_objective = float(v_input)		
			break
		except NameError,ValueError:
	   		print("That's not a number!")
	#arm drone
	arm_drone(vehicle)

	#calculate input in degrees for use in local functions (LocationGlobal)
	degrees = calculate_degrees_with_distance(vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.lat, x_objective, y_objective)

	#calculate target (lon,lat)
	target_lon = degrees[0]
	target_lat = degrees[1]

	# Set the LocationGlobal to head towards
	print "Actual Global Location (Relative): %s" % vehicle.location.global_relative_frame
	print "target Position: lon = %f and lat = %f " % (target_lon, target_lat)

	#setting parameters and goto call
	a_location = LocationGlobalRelative(target_lat, target_lon, z_objective)
	initial_lon = vehicle.location.global_relative_frame.lon 
	initial_lat = vehicle.location.global_relative_frame.lat
	initial_alt = vehicle.location.global_relative_frame.alt
	vehicle.airspeed = v_objective
	vehicle.simple_goto(a_location)

	#check position in relation to objective
	while (True):
		#show status
		print "\n trajectory status: "
		print "target distance in degrees: lon = %f and lat = %f " % (target_lon, target_lat)
		print "Actual Global Location in degrees: lon = %f and lat = %f " % (vehicle.location.global_relative_frame.lon, vehicle.location.global_relative_frame.lat)
		#calculate distance in m
		distance = calculate_distance_in_m(initial_lon, vehicle.location.global_relative_frame.lon, initial_lat, vehicle.location.global_relative_frame.lat)
		print "distance travelled in m: x = %f, y = %f" % (distance[0], distance[1])
		#show altitude	
		print "altitude: initial = %f, actual = %f, target = %f " % (initial_alt, vehicle.location.global_relative_frame.alt, z_objective)	
		time.sleep(1)
		#if target is reached, break
		delta_lon = vehicle.location.global_relative_frame.lon - target_lon
		delta_lat = vehicle.location.global_relative_frame.lat - target_lat
		delta_alt = vehicle.location.global_relative_frame.alt - z_objective
		if (math.fabs(delta_lon) < Constants.MAX_DIFFERENCE_DEGREES and math.fabs(delta_lat) < Constants.MAX_DIFFERENCE_DEGREES and math.fabs(delta_alt) < Constants.MAX_DIFFERENCE_ALTITUDE):
			print "destination reached"
			break
