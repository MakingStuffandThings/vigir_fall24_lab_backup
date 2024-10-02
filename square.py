#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry 

import math
from  tf.transformations import euler_from_quaternion

sides=4
length=0.5

def callback(data):
    global odom_x,odom_y,O_z
    location = data.pose.pose
    odom_x = location.position.x
    odom_y = location.position.y
    quaternion = [location.orientation.x,
                location.orientation.y, 
                location.orientation.z, 
                location.orientation.w]
    e = euler_from_quaternion(quaternion)
    O_z = e[2]
                

def odom():
    rospy.init_node('odom', anonymous = True)
    rospy.Subscriber('/odom',Odometry, callback)


def square():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1) 
    rospy.sleep(2)
    i = 0

    while(i < 4):
        i = i + 1
        last_x = odom_x
        last_y = odom_y
        last_O_z = O_z





        #linear
        twist_msg = Twist()
        twist_msg.linear.x = 0.1
        twist_msg.angular.z = 0.0

        rospy.loginfo(twist_msg)
        pub.publish(twist_msg)
        print('length' + str(i))
        
        while(True):
            if ((abs(odom_x - last_x) >= length) or (abs(odom_y - last_y) >= length)):
                break    
            
        
        #angular
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0.1
        rospy.loginfo(twist_msg)
        pub.publish(twist_msg)
        print('turn' + str(i))

        while(True):
            if not (abs(O_z-last_O_z) <= ((math.pi)*2)/sides):
                break
                
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    rospy.loginfo(twist_msg)
    pub.publish(twist_msg)
    

if __name__ == '__main__':
    try:
        odom()
        rospy.sleep(1)
        square()
    except rospy.ROSInterruptException:
        print('exception')
        pass

