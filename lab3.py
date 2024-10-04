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


#step 1, create ro, alpha, beta
# step 2, using those, construct a homogenous matrix
#[cos(theta) -sin(theta) 0    delta(x)    ]
#[sin(theta)  cos(theta) 0    delta(y)    ]
#[0           0          1    delta(theta)]
#[0           0          0    1           ]

#save this matrix as a variable when calculating the first time
#after this multiply this matrix by
#[0]
#[0]
#[0]
#[1]
#hardocode the D[]S matrix with desired values

#[cos(-90) -sin(-90)   0    -2   ]   [0]
#[sin(-90)  cos(-90)   0     1   ] * [0]
#[0         0          1     0   ]   [0]
#[0         0          0     1   ]   [1]
#this this will give us the first Velocity=v and Rotation=w to get where you need to go
#
#use matrix [v] = [Kp 0   0  ]*[p] where K is some speed value that we apply as a global set speed multiplier
#           [w]   [0  Ka  Kb ] [a]
#                              [b]
#[p]
#[a] are given from somewhere idk anymore man
#[b]
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#








def calc_p(x,y):
    return math.sqrt( pow(deltaX(x),2) + pow(deltaY(y))   )

def calc_alpha(theta,x,y):
    return (theta*-1)+Numpy.atan2(deltaY(y),deltaX(x))
def calc_w(theta):
    return theta
def calc_b():










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

        #hello, this is a comment



















    ''' 
        #linear
    
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
    '''
                
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    rospy.loginfo(twist_msg)
    pub.publish(twist_msg)
    

if __name__ == '__main__':
    try:
        odom()
        rospy.sleep(1)
        program()
    except rospy.ROSInterruptException:
        print('exception')
        pass

