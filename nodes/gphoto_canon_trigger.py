#!/usr/bin/env python
'''
'''
from optparse import OptionParser
import roslib
import rospy
import os
import time

from std_msgs.msg import Int32, String

'''
sudo apt-get install libgphoto2-dev
sudo pip install -v gphoto2 (takes a while, be patient)
To test, you can use: rosrun multi_tracker republish_pref_obj_data.py --rate=0.1 --simulate
'''
import gphoto2 as gp

import gphoto_canon_trigger_utils.gphoto_utils as gphoto_utils
            
# The main tracking class, a ROS node
class GPhotoCamera:
    def __init__(self, directory_name, trigger_topic, publisher_topic, serial):
        nodenum = 'N1'

        self.context = gp.Context()

        # define and make directory
        directory_name = os.path.expanduser(directory_name)
        self.destination = directory_name
        if os.path.exists(self.destination):
            pass
        else:
            os.mkdir(self.destination)

        # initialize the node
        rospy.init_node('gphoto2_' + nodenum)
        self.nodenum = nodenum
        self.triggers = 0

        #gp.check_result(gp.use_python_logging())
        self.camera = gphoto_utils.get_camera(serial)
        self.synchronize_camera_timestamp()
        
        self.subTrigger = rospy.Subscriber(trigger_topic, Int32, self.gphoto_callback)
        self.pubNewImage = rospy.Publisher(publisher_topic, String, queue_size=5)



    def synchronize_camera_timestamp(self):
        def set_datetime(config):
            OK, date_config = gp.gp_widget_get_child_by_name(config, 'datetime')
            if OK >= gp.GP_OK:
                widget_type = gp.check_result(gp.gp_widget_get_type(date_config))
                if widget_type == gp.GP_WIDGET_DATE:
                    now = int(time.time())
                    gp.check_result(gp.gp_widget_set_value(date_config, now))
                else:
                    now = time.strftime('%Y-%m-%d %H:%M:%S')
                    gp.check_result(gp.gp_widget_set_value(date_config, now))
                return True
            return False

        # get configuration tree
        config = gp.check_result(gp.gp_camera_get_config(self.camera, self.context))#, self.context))
        # find the date/time setting config item and set it
        if set_datetime(config):
            # apply the changed config
            gp.check_result(gp.gp_camera_set_config(self.camera, config, self.context))#, self.context))
        else:
            print('Could not set date & time')
        # clean up
        gp.check_result(gp.gp_camera_exit(self.camera,self.context))#, self.context))
        return 0



    def gphoto_callback(self, msg):
        if self.triggers < 500: # max number of picturs to take
            #print('Captured image')
            t = rospy.Time.now()
            time_base = time.strftime("%Y%m%d_%H%M%S_N" + self.nodenum, time.localtime())
            name = time_base + '_' + str(t.secs) + '_' + str(t.nsecs) + '.jpg'
            destination = os.path.join(self.destination, name)

            gphoto_utils.trigger_capture_and_save(self.camera, destination)

            self.pubNewImage.publish(String(destination))
            self.triggers += 1
        
    def Main(self):
        while (not rospy.is_shutdown()):
            rospy.spin()

#####################################################################################################
    
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--directory_name", type="str", dest="directory_name", default='~/gphoto2',
                        help="Directory where images will be saved")
    parser.add_option("--trigger_topic", type="str", dest="trigger_topic", default='gphoto_trigger',
                        help="Rostopic that will trigger photos anytime there is something published")
    parser.add_option("--publisher_topic", type="str", dest="publisher_topic", default='gphoto_filenames',
                        help="Topic where filenames will be published")
    parser.add_option("--serial", type="str", dest="serial", default='',
                        help="Serial number for the camera you want to trigger. This may not work for all cameras. Tested on Canon 5D2 and Rebel SL2")
    (options, args) = parser.parse_args()
    
    gphotocamera = GPhotoCamera(options.directory_name, options.trigger_topic, options.publisher_topic, options.serial) #options.nodenum, options.topic, options.serial)
    gphotocamera.Main()
