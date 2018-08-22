from gopigo import *
import time
import random

min_distance = 100

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

stop()
enable_servo()
servo(90)
time.sleep(3)
autonomy()