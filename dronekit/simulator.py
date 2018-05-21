print "Start simulator (SITL)"
import dronekit_sitl
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()
print "Connecting to vehicle on: %s" % (connection_string)
# Shut down simulator
while True:
	if raw_input("enter c to close: "):
		sitl.stop()
		break
