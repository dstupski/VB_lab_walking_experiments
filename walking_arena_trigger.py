#!/usr/bin/env python
import serial
import roslib, rospy
from std_msgs.msg import Int32MultiArray, Float64, Float64MultiArray
import time
import numpy as np
import random
import sympy as sym
from optparse import OptionParser
from std_msgs.msg import Int32MultiArray
import numpy as np
from optparse import OptionParser
import yaml
import time as time
from multi_tracker.msg import Contourinfo, Contourlist
from multi_tracker.msg import Trackedobject, Trackedobjectlist
from multi_tracker.srv import resetBackgroundService, addImageToBackgroundService
global tcall
rospy.init_node('demo2listener2', anonymous =True)
tcall = rospy.get_time()
tnow =rospy.get_time()
tseconds = 5
tdur =5.0
testpos =0.0
counter = 0
state1 =0
state2 = 0
frame_n =0
t1 = 0
refrac =300
0
light_state =0
arduino = serial.Serial(port='/dev/ledsys', baudrate=9600, timeout=.1)
pub = rospy.Publisher("Trigger_time", Float64MultiArray )
msg=Float64MultiArray()

def callback1(data):
	#print(data.position)
	table= str(data) 
	pos= table.find("y:")
	tpos= table.find('"')
	tpos2 = table.find("position:")
	#print(table)
	t1= table[tpos+2:tpos+16]
	ypos1 = float((table[pos+2:pos+6]))
	testpos=ypos1
	#print("arena 1")
	#print(table[tpos+1:tpos2-6])
	if ypos1 < 500:
		global state1
		state1=1
	else:
		state1=0
	#print("T1 " + str(t1))

def callback2(data):
	#print(data.position)
	table2= str(data)
	#print(table2)
	pos2= table2.find("y:")
	ypos2 = float((table2[pos2+2:pos2+6]))
	tpos3= table2.find('"')
	tpos4 = table2.find("position:")
	global frame_n 
	frame_n= float(table2[tpos3+1:tpos4-6])
	tnow= rospy.get_time()
	#print(table2)
	#print("Arena 2")
	#print(table2[tpos3+1:tpos4-6])

	if ypos2 < 500:
		state2 =1
	else:
		state2 =0
	#print("state 1 is " +str(state1))
	#print("state 2 is " +str(state2))
	if state1==1 and state2 ==1 and light_state==0 and tnow> tcall + refrac:
		arduino.write('y')
		msg.data=[1.0, frame_n]
		pub.publish(msg)
		global light_state
		light_state = 1
		global tcall
		tcall = rospy.get_time()

	if light_state ==1 and tnow > tcall + tdur:
		arduino.write('n')
		msg.data =[0, frame_n]
		pub.publish(msg)
		global light_state
		light_state = 0 


	
def listener2():
	#rospy.init_node('demo2listener2', anonymous =True)
	rospy.Subscriber('/multi_tracker/2/tracked_objects', Trackedobjectlist, callback2)
	#rospy.init_node('demo1listener', anonymous =True)
	rospy.Subscriber('/multi_tracker/1/tracked_objects', Trackedobjectlist, callback1)
	rospy.spin()


#while(True):
#	print(state1)
#	arduino.write('y')
#	time.sleep(2)
#	arduino.write('n')
#	tcall = time.time()
#def flash_check(tflash, tsleep):
##	if state1 == 1 and state2 == 1:
#		arduino.write('y')
#		print("boom")
##		time.sleep(tflash)
#		arduino.write('n')
#		time.sleep(tsleep)
#	return



if __name__ == '__main__':
	#listener1()
	listener2()
	rospy.spin()
#	flash_check(5, tseconds)

	

