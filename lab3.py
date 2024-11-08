#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry 
import numpy

import math
from  tf.transformations import euler_from_quaternion

goals=4
length=0.5


goal_coords=[(-0.5,1,-90),(-1,0.5,180),(-1,-0.5,270),(1,-0.5,0)]


source_coords=[(0,0,0),(1,0.5,math.pi/2),(-1,0.5,math.pi),(-1,-0.5,((math.pi)/2)*3),(1,-0.5,0)]


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
    #O_z=location.orientation.z
                

def odom():
    rospy.init_node('odom', anonymous = True)
    rospy.Subscriber('/odom',Odometry, callback)

#Todo: debug alpha not shrinking as angle gets corrected
       
#
#step:1
#
# #construct matrix dHs
# [cos(dtheta) -sin(dtheta) 0 dx]
# [sin(dtheta)  cos(dtheta) 0 dy]
# [0            0           1  0]
# [0            0           0  1] 


#construct cHs
# where c= abs(odom_curent-odom_last)
# [cos(ctheta) -sin(ctheta) 0   cx]
# [sin(ctheta)  cos(ctheta) 0   cy]
# [0            0           1   0 ]
# [0            0           0   1 ]


#construct dHc by multiplying dHs * (cHs)^-1

#extract x y z from dHc, convert to spherical coords
#use matrix 

# where k is some modifier set by us
# [ u ] = [Kp 0 0 ] *[p]
# [ w ]   [0 Ka Kb]  [a]
#                    [b]
#publish u as linear.x and w as angular.z,
#using while(dest-current>tolerance)
kp=0 #0.09
ka=0.2
kb=-0.1
def calc_gain_matrix(p,a,b):
    input_vector=numpy.array([p,a,b])

    gain_matrix=numpy.array([[kp,0,0],
                            [0,ka,kb]])
    robot_vals=numpy.matmul(gain_matrix,input_vector)
    print(robot_vals)
    return robot_vals



def cartesian_to_polar(x, y, t):
    #calculate r
    r = math.sqrt(math.pow(x,2) + math.pow(y,2))
    #calculate alpha
    print("The value from atan2(y,x)=",math.degrees(math.atan2(y,x)),"The theta=",math.degrees(t))
    alpha = (-t)+(math.atan2(y, x))
    
    #calcualte beta
    beta=-(t+alpha)
    
    return r, alpha, beta
def build_transform (x,y,theta):

    cos = math.cos (math.radians(theta))
    sin = math.sin (math.radians(theta))
    #cos = round (cos, 1)

    m1 = numpy.array([[cos,-sin,0,x],[sin,cos,0,y],[0,0,1,0],[0,0,0,1]])

    print (m1)
    return m1

def source_minus_odom(x,y,theta):
    return (x-odom_x,y-odom_y,theta-O_z)

def program():
  
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
    rate = rospy.Rate(10)
    rospy.sleep(2)
    i = 0

    #while(i < goals):

    # i = i + 1
    last_x=odom_x
    last_y=odom_y
    last_theta=O_z
    twist_msg = Twist()
    p_a_b=[10,10,10]

    while(p_a_b[0]>=0.01):
        #print("dest coords are \n",goal_coords[0],"\n")
        #print("dhs is")
        dHs=build_transform(goal_coords[i][0],goal_coords[i][1],goal_coords[i][2])
        #dHs=build_transform(1,1,90)
        c_val=source_minus_odom(source_coords[i][0],source_coords[i][1],source_coords[i][2])
        #print("Values from odom are x=",odom_x," y=",odom_y," theta(radians)=",O_z,"\n")
        #print("Values from odom-source",c_val)
        
        cHs=build_transform(c_val[0],c_val[1],c_val[2])
        #cHs=build_transform(odom_x,odom_y,O_z)
        cHs_inv =cHs #numpy.linalg.inv(cHs)
        #print("dHc is \n")
        dHc=numpy.matmul(dHs,cHs_inv)
        column_4 = dHc[0:3, 3]
        column_4_matrix = column_4.reshape(3, 1)
        rate.sleep()
        


       

        print(dHc)
        theta=O_z#math.atan2(dHc[1][0],dHc[0][0])
        #print("X wrt dHc",column_4_matrix[0],"Y wrt dHc",column_4_matrix[1],"Theta wrt dHc",theta)
        p_a_b=cartesian_to_polar(column_4_matrix[0],column_4_matrix[1],theta)
        print("p=",p_a_b[0],"a=",math.degrees(p_a_b[1]),"b=",math.degrees(p_a_b[2]))
        
        u_w=calc_gain_matrix(p_a_b[0],p_a_b[1],p_a_b[2])
        
        print("Command velocity and theta are: ",u_w)
        print("\n\n\n\n\n")
        rospy.sleep(0.5)
        twist_msg.linear.x = 0
        twist_msg.angular.z = 0
        pub.publish(twist_msg)
        
        input("press any key to send to robot")
        twist_msg.linear.x = u_w[0]
        twist_msg.angular.z = u_w[1]
        rospy.loginfo(twist_msg)
        pub.publish(twist_msg)
        








      
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    rospy.loginfo(twist_msg)
    pub.publish(twist_msg)




      
        
       
    twist_msg.angular.z = 0
    rospy.loginfo(twist_msg)
    pub.publish(twist_msg)
    

if __name__ == '__main__':
    try:
        
        odom()
        rospy.sleep(1)
        program()
        
       
        



       
        # calc_gain_matrix(1,2,3,1)
    except rospy.ROSInterruptException:
        print('exception')
        pass

