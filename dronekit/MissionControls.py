from dronekit import VehicleMode, Command

def showWaypoints(vehicle):
	cmds = vehicle.commands
	cmds.download()	
	cmds.wait_ready()
	num_cmds = cmds.count
	if (num_cmds == 0):
		return "no waypoints inserted!"
	num_waypoint = 0
	for cmd in cmds:
		print "waypoint %i: %s" % (num_waypoint,cmd)
		num_waypoint += 1
	return " "