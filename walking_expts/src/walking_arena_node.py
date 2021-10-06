#!/usr/bin/env python

# Command line arguments
from optparse import OptionParser

# ROS imports
import roslib, rospy

# numpy imports - basic math and matrix manipulation
import numpy as np
import time

import yaml

from std_msgs.msg import Float32, Float32MultiArray, Float64MultiArray
from multi_tracker.msg import Contourinfo, Contourlist
from multi_tracker.msg import Trackedobject, Trackedobjectlist
import serial

arena_id_dict ={'1':('a', 'b'), '2':('c', 'd'), '3':('e', 'f')}
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
		self.onbyte = arena_id_dict[self.arena_id][0]
		self.offbyte =arena_id_dict[self.arena_id][1]
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
		table= str(data) 
		pos= table.find("y:")
		tpos= table.find('"')
		t1= table[tpos+2:tpos+16]
		tpos3= table.find('"')
		tpos4 = table.find("position:")
		frame_n= float(table[tpos3+1:tpos4-6])
		ypos1 = float((table[pos+2:pos+6]))
		if self.trigger_state ==0 and ypos1 < self.max_y and ypos1 >self.min_y and tcall > self.last_trigger + self.refrac:
			self.arduino.write(self.onbyte)
			self.last_trigger = tcall
			self.trigger_state = 1
			self.beg_frame= frame_n

		elif self.trigger_state==1 and tcall > self.last_trigger + self.trigger_dur:
			self.arduino.write(self.offbyte)
			self.trigger_state =0
			toff= time.time()
			self.end_frame = frame_n
			self.msg.data =[self.last_trigger, toff, self.beg_frame, self.end_frame]
			self.trigger_pub.publish(self.msg)

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


