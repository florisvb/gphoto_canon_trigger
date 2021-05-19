#!/usr/bin/env python

from std_msgs.msg import Int32
import rospy
from optparse import OptionParser



if __name__ == '__main__':
    parser = OptionParser()
    (options, args) = parser.parse_args()

    rospy.init_node('test_gphoto_trigger_' + options.nodenum)

    rospy.sleep(2)
    
    publisher = rospy.Publisher('/trigger_gphoto', Int32, queue_size=1)
    msg = Int32()
    msg.data = 1

    for i in range(2):
        publisher.publish(msg)
        rospy.sleep(1)
        print(msg)