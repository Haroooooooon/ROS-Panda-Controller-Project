#!/usr/bin/env python

import rospy
import random

from AR_week8_test.msg import square_size


def square_size_generator():
    # initialise new topic
    pub = rospy.Publisher('size', square_size, queue_size=0)
    # initialise new node
    rospy.init_node('square_size_generator', anonymous=True)
    rate = rospy.Rate(0.05)
    msg = square_size()
    while not rospy.is_shutdown():
        msg.size = random.uniform(0.05, 0.20)
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        square_size_generator()
    except rospy.ROSInterruptException:
        pass
