from dronekit import VehicleMode, Command
from MyConnect import my_connect
from pymavlink import mavutil
from GotoMeters import add_goto_mission, calculate_distance_in_m
import time
from LandingTakeoff import takeoff
import Constants
from math import fabs

#connection_string = sitl.connection_string()
connection_string = "tcp:127.0.0.1:5760"
vehicle = my_connect(connection_string)

# Get the set of commands from the vehicle
cmds = vehicle.commands
cmds.clear()
cmds.upload()

while True:
	try:
		#alt_input = raw_input("type a altitude for takeoff (for mission, in case of failure of main method)[m]: ")
		#alt_objective = float(alt_input)
		v_airspeed_input = raw_input("type the copter speed[m/s]: ")
		v_airspeed = float(v_airspeed_input)	
		break
	except NameError,ValueError:
   		print("That's not a number!")

#
vehicle.airspeed = v_airspeed

#base lon and lat
base_lon = vehicle.location.global_relative_frame.lon
base_lat = vehicle.location.global_relative_frame.lat

#Add MAV_CMD_NAV_TAKEOFF command. This is ignored if the vehicle is already in the air.
#cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, 0, alt_objective))
add_goto_mission(vehicle)
#copies last mission, for mission control purposes
#cmds.download()
#cmds.wait_ready()
cmds.add(cmds[cmds.count - 1])
#cmds.add(Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0, base_lat, base_lon, 0))
#cmds.upload()		
#add_goto_mission(vehicle)
#cmds.download()
#cmds.wait_ready()
print "commands: "
for cmd in cmds:
	print cmd

print "count pretakeoff: %i" % cmds.count

#delay for better erminal visibility
time.sleep(1)
takeoff(vehicle)

print "count posttakeoff: %i" % cmds.count

print "commands: ",
for cmd in cmds:
	print cmd

print "Starting mission"
# Reset mission set to first (0) waypoint
cmds.next=0

# Set mode to AUTO to start mission
vehicle.mode = VehicleMode("AUTO")

while True:
	currentMission = cmds.next -1
	missionitem = cmds[currentMission] #commands are zero indexed
	print "currentMission: %i" % currentMission
	print "count: %i" % cmds.count
	if currentMission == (cmds.count - 1):
		break
	distance = calculate_distance_in_m(vehicle.location.global_relative_frame.lon, missionitem.y, vehicle.location.global_relative_frame.lat, missionitem.x)
	height = vehicle.location.global_relative_frame.alt - missionitem.z
	distance = distance + (height,)
	print "distances: lon = %f, lat = %f, alt = %f " % distance
	time.sleep(1)

'''
test loop
while True:
	missionitem = cmds[nextwaypoint-1] #commands are zero indexed
	distance = calculate_distance_in_m(vehicle.location.global_relative_frame.lon, missionitem.y, vehicle.location.global_relative_frame.lat, missionitem.x)
	height = vehicle.location.global_relative_frame.alt - missionitem.z
	distance = distance + (height,)
	print "distances: lon = %f, lat = %f, alt = %f " % distance
	time.sleep(1)
'''

print "executing RTL"
vehicle.mode = VehicleMode("RTL")

while True:
	distance = calculate_distance_in_m(vehicle.location.global_relative_frame.lon, base_lon, vehicle.location.global_relative_frame.lat, base_lat)
	height = vehicle.location.global_relative_frame.alt
	distance = distance + (height,)
	print "distances: lon = %f, lat = %f, alt = %f" % distance
	if fabs(vehicle.location.global_relative_frame.alt) <= Constants.MAX_DIFFERENCE_ALTITUDE:
		break
	time.sleep(1)
#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close()
