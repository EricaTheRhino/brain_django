import dbus
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
import gobject
import requests
import os, sys
import json

fpid = os.fork()
if fpid != 0:
	sys.exit(0)

cache = {}

filtered = [
	"00:80:98:EA:D3:CD",
	"00:80:98:E9:1F:BB",
	"00:1E:C2:9B:B6:A0",
	"00:25:BC:68:E9:F6",
	"00:1F:5B:E1:D0:C0"
]
bus = dbus.SystemBus()
manager = dbus.Interface(bus.get_object("org.bluez", "/"), "org.bluez.Manager")
adapter = dbus.Interface(bus.get_object("org.bluez", manager.DefaultAdapter()), "org.bluez.Adapter")

def handleFound(address, values):
	global cache
	global filtered
	if not address in cache and not address in filtered:
		print address
		print values
		requests.post("http://localhost/events/", data=json.dumps({'event':'environment.bluetooth.found', 'params':{'address':address}}))
		cache[address] = True

def handleLost(address):
	global cache
	if address in cache:
		del cache[address]
		requests.post("http://localhost/events/", data=json.dumps({'event':'environment.bluetooth.lost', 'params':{'address':address}}))

adapter.connect_to_signal('DeviceFound', handleFound)
adapter.connect_to_signal('DeviceDisappeared', handleLost)
print "* Start discovery"
adapter.StartDiscovery()
print "* Entering main loop"
gobject.MainLoop().run()

