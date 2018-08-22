from gopigo import *
import time
import random
import usb.core
import usb.util
import os
import platform

min_distance = 100
model_b_plus = True

# protocol command bytes
DOWN = 0x01
UP = 0x02
LEFT = 0x04
RIGHT = 0x08
FIRE = 0x10
STOP = 0x20

DEVICE = None
DEVICE_TYPE = None

# set up the office cannon
def setup_usb():
	global DEVICE
	global DEVICE_TYPE

	DEVICE = usb.core.find(idVendor=0x2123, idProduct=0x1010)

	if DEVICE is None:
		DEVICE = usb.core.find(idVendor=0x0a81, idProduct=0x0701)
		if DEVICE is None:
			raise ValueError("Missile device not found")
		else:
			DEVICE_TYPE = "Original"
	else:
		DEVICE_TYPE = "Thunder"

	# on linux we need to detach usb HID first
	if "Linux" == platform.system():
		try:
			DEVICE.detach_kernel_driver(0)
		except Exception, e:
			pass #already unregistered
	DEVICE.set_configuration()

# send command to office cannon
def send_cmd(cmd):
	if "Thunder" == DEVICE_TYPE:
		DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x02, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
	elif "Original" == DEVICE_TYPE:
		DEVICE.ctrl_transfer(0x21, 0x09, 0x200, 0, [cmd])

# send command to control LED on the office cannon
def led(cmd):
	if "Thunder" == DEVICE_TYPE:
		DEVICE.ctrl_transfer(0x21, 0x09, 0, 0, [0x03, cmd, 0x00,0x00,0x00,0x00,0x00,0x00])
	elif "Original" == DEVICE_TYPE:
		print("there is no LED on this device")	

# send command to move office cannon
def send_move(cmd, duration_ms):
	send_cmd(cmd)
	time.sleep(duration_ms / 1000.0)
	send_cmd(STOP)

def autonomy():

        no_problem = True

        while no_problem:

                servo(90)
                time.sleep(1)
                dist = us_dist(15)

                if dist > min_distance:
                        print('moving forward ', dist)
                        fwd()
                        time.sleep(.75)

                else:
                        print('stuff is in the way ', dist)
                        stop()
			
			# fire the cannon!
			time.sleep(0.5)
			send_cmd(FIRE)
			time.sleep(4.5)

                        servo(165)
                        time.sleep(1)
                        left_dir = us_dist(15)
                        time.sleep(1)

                        servo(30)
                        time.sleep(1)
                        right_dir = us_dist(15)
                        time.sleep(1)

			if left_dir > right_dir and left_dir > min_distance:
				print('turning left')
				left()
				time.sleep(.75)

			elif left_dir < right_dir and right_dir > min_distance:
				print('turning right')
				right()
				time.sleep(.75)

			else:
				print('no good option, reversing')
				bwd()
				time.sleep(1.5)
				rot_choices = [right_rot, left_rot]
				rotation = rot_choices[random.randrange(0,2)]
				rotation()
				time.sleep(.75)

		stop()

setup_usb()
# enable usb to give supply up to 1.2A on model B+
if model_b_plus:
	os.system("gpio -g write 38 0")
	os.system("gpio -g mode 38 out")
	os.system("gpio -g write 38 1")

stop()
enable_servo()
servo(90)
time.sleep(3)
autonomy()