#!/usr/bin/env python3
import rospy
from kobuki_msgs.msg import BumperEvent

def callback(data):
    print(data)
    # Contact sensors
    global is_left_pressed, is_right_pressed
    
    # Bumper light sensors (Create 2 only) in order from left to right
    # Value = true if an obstacle detected
    global is_light_left, is_light_front_left, is_light_center_left
    global is_light_right, is_light_front_right, is_light_center_right

    # Raw light sensor signals
    # Values in range [0, 4095]
    global light_signal_left, light_signal_front_left, light_signal_center_left
    global light_signal_right, light_signal_front_right, light_signal_center_right
    
def oa():
    rospy.init_node('OA_node', anonymous = True)
    rospy.Subscriber('/bumper', BumperEvent, callback)

    if is_left_pressed:
        
        return
    if is_right_pressed:

        return

if __name__ == '__main__':
    try:
        oa()
        rospy.sleep(1)
    except rospy.ROSInterruptException:
        print('exception')
        pass
