#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry 
import Numpy

import math
from  tf.transformations import euler_from_quaternion

goals=4
length=0.5

goal_coords=[(0,2,math.pi/2),(0,0,math.pi),(1,0,((math.pi)/2)*3),(1,2,0)]


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

def deltaX(x):
    return abs(odom_x-x)
def deltaY(y):
    return abs(odom_y-y)
def deltaTheta(z):
    return abs(O_z-z)



def calc_p(x,y):
    return math.sqrt( pow(deltaX(x),2) + pow(deltaY(y))   )

def calc_alpha(theta,x,y):
    return (theta*-1)+Numpy.atan2(deltaY(y),deltaX(x))
def calc_w(theta):
    return theta
def calc_b():
    return

def program():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
    rospy.sleep(2)
    i = 0





    while(i < goals):
        i = i + 1
        last_x = odom_x
        last_y = odom_y
        last_O_z = O_z
        twist_msg = Twist()


    
    
    
    
    
    
    return



if __name__ == '__main__':
    try:
        odom()
        rospy.sleep(1)
        program()
    except rospy.ROSInterruptException:
        print('exception')
        pass

