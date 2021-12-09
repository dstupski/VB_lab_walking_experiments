#!/usr/bin/env python

# Command line arguments
from optparse import OptionParser

# ROS imports
import roslib, rospy

# numpy imports - basic math and matrix manipulation
import numpy as np
import time
import random
import yaml

from std_msgs.msg import Float32, Float32MultiArray, Float64MultiArray
from multi_tracker.msg import Contourinfo, Contourlist
from multi_tracker.msg import Trackedobject, Trackedobjectlist
import serial
#Set up a dictionary that can assign an array of unique letter/number combinations
#this will allow us to identify which arena were working with in the configuration file and for each instance of this node
#it will only write bytes to the arduino that will control the correct control for that individual arena
#e.g. if the configuration file denotes the arena number as "2" it will only send bytes that the arduino firmware can use to manipulate the second arena
#Somewhat odd structure but worked well for integrating multiple nodes in one place 
#I did it this way to have fewer things to specify in the configuration file
arena_id_dict ={'1':[('a', 0), ('b', 40), ('c', 200), ('d', 1000), ('e', 5000)], '2':[('f', 0), ('g', 40), ('h', 200), ('i', 1000), ('j', 5000)], '3':[('k', 0), ('l', 40), ('m', 200), ('n', 1000), ('o', 5000)]}
class walkingTrigger:
	def __init__(self,config_file):
		#collate configuration file parameters into variables
		with open(config_file) as file:
			self.config = yaml.load(file)
		self.min_y = self.config['min_y']
		self.max_y = self.config['max_y']
		self.trigger_dur=self.config['trigger_dur']
		self.pub_node = self.config['pub_node']
		self.sub_node = self.config['sub_node']
		self.arena_id=self.config['arena_id']
		#self.onbyte = arena_id_dict[self.arena_id][0]
		#self.offbyte =arena_id_dict[self.arena_id][1]
		self.trigger_array = arena_id_dict[self.arena_id]
		#make a subcribe node that looks at the tracked objects from the node specified in the configuration file
		self.tracker_sub=rospy.Subscriber(self.sub_node, Trackedobjectlist, self.callback)
		#make a publisher that will publish all the information from a light trigger including frame number, position of the fly, and fly objid
		self.trigger_pub=rospy.Publisher(self.pub_node, Float64MultiArray)
		self.last_trigger= time.time()
		self.trigger_state =0
		self.refrac = self.config['refrac']
		self.arduino = serial.Serial(port=self.config['port'], baudrate=self.config['baud'], timeout=.1)
		self.msg = Float64MultiArray()
		self.beg_frame =0
		self.end_frame= 0
	def test_func(self):
		print(self.onbyte)
	def callback(self, data):
		tcall = time.time()
		#try:
		table= str(data) 
		pos= table.find("y:")
		tpos= table.find('"')
		t1= table[tpos+2:tpos+16]
		tpos3= table.find('"')
		tpos4 = table.find("position:")
		frame_n= float(table[tpos3+1:tpos4-6])
		ypos1 = float((table[pos+2:pos+6]))
		#print(ypos1)
		if ypos1 < self.max_y and ypos1 >self.min_y and tcall > self.last_trigger + self.refrac:
			    
			on_trig = random.choice(self.trigger_array)
			#print("I should be doing something")
			on_byte =on_trig[0]
			on_dur =on_trig[1]
			self.arduino.write(on_byte)
			self.last_trigger = tcall
			self.trigger_state = 1
			self.beg_frame= frame_n
			self.msg.data=[self.beg_frame, tcall, on_dur]
			self.trigger_pub.publish(self.msg)
		#except:
		#    print("arduino is fucking me up bruh")
		#elif self.trigger_state==1 and tcall > self.last_trigger + self.trigger_dur:
		#	self.arduino.write(self.offbyte)
		#	self.trigger_state =0
		#	toff= time.time()
		#	self.end_frame = frame_n
		#	self.msg.data =[self.last_trigger, toff, self.beg_frame, self.end_frame]
		#	self.trigger_pub.publish(self.msg)

	def run(self):
		rospy.init_node('testy_test', anonymous= True)
		rospy.spin()

		

if __name__ == '__main__':
	parser= OptionParser()
	parser.add_option("--config", type="str", dest="config", default='',
                        help="Full path that points to a config.yaml file. See ../configs/volume_trigger_config.yaml for an example")
	(options, args) = parser.parse_args()
	walk_trigger = walkingTrigger(config_file=options.config)
	#walk_trigger.test_func()
	walk_trigger.run()


