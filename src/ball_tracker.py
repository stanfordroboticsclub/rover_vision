#!/usr/bin/env python

# subscribes to camera feed
# do image processing
# publishes bounding box

# camera/image_raw
#
# camera/bound_box

# roslaunch rover_vision gscam.launch
# rosrun image_view image_view image:=/camera/image_raw

from __future__ import print_function

import roslib
import rospy
import numpy as np
import sys
import cv2
import imutils
import time

from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from collections import deque


class ball_tracker:

	greenLower = (20, 86, 6)
	greenUpper = (64, 255, 255)
	
	
	#pts = deque(1000)

	def __init__(self):
		self.image_pub = rospy.Publisher('bound_box',Image,queue_size=10)

		self.bridge = CvBridge()
		self.image_sub = rospy.Subscriber('camera/image_raw',Image,self.callback)

	def callback(self,data):
		# convert ROS image to OpenCV image
		try:
			frame = self.bridge.imgmsg_to_cv2(data, 'bgr8')
			# unclear if input data is rgb or bgr
		except CvBridgeError as e:
			print(e)

		print(frame[100,100])
		# resize the frame, blur it, and convert it to the HSV
		# color space
		frame = imutils.resize(frame, width=600)
	        #blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None

		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			cs = sorted(cnts, key=cv2.contourArea)
	                for c in cs[-2:]:
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

				# only proceed if the radius meets a minimum size
				if radius > 2:
					# draw the circle and centroid on the frame,
					# then update the list of tracked points
					cv2.circle(frame, (int(x), int(y)), int(radius),
						(0, 255, 255), 2)
					# draw bounding box
					#cv2.rectangle(frame,)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
					#print(center)

		# update the points queue
		#self.pts.appendleft(center)

		# convert and publish ROS image
		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(frame, 'rgb8'))
		except CvBridgeError as e:
			print(e)

def main():
	rospy.init_node('ball_tracker', anonymous=True)
	bt = ball_tracker()
	rospy.spin()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()
