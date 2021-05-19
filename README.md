# Simple ROS node for triggering Canon dSLRs

### Install dependencies
1. `sudo apt-get install libgphoto2-dev`
2. `sudo pip install -v gphoto2` (takes a while, be patient)

### Install the utility
1. from this directory, run `python ./setup.py install`

### Test the system
1. plug in Canon SLR (e.g. 5D2) with USB
2. test that everything is working: run `nodes/check_gphoto_cameras.py` to automatically find the camera, trigger a capture, and download the file
3. optional (if using multiple cameras): note the serial number that is printed when you run the test, ie. `8cb6612c6f94d87`

### Run a ROS node and trigger with ROS
1. run `roscore`
1. run the ROS node: `rosrun gphoto_canon_trigger gphoto_canon_trigger.py`, optionally specify serial, directory to save photos, and topic names (see `rosrun gphoto_canon_trigger gphoto_canon_trigger.py --help`)
2. publish something (any floating integer) on the trigger topic (the default of which is `/gphoto_trigger`). for example: `rostopic pub /gphoto_trigger std_msgs/Int32 1`