#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry 
import numpy

import math
from  tf.transformations import euler_from_quaternion

goals=4
length=0.5


goal_coords=[(1,0.50,90),(-1,0.5,180),(-1,-0.5,270),(1,-0.5,0)]


source_coords=[(0,0,0),(1,0.5,math.pi/2),(-1,0.5,math.pi),(-1,-0.5,((math.pi)/2)*3),(1,-0.5,0)]


def callback(data):
    global odom_x,odom_y,O_z
    location = data.pose.pose
    odom_x = location.position.x
    odom_y = location.position.y
    '''quaternion = [location.orientation.x,
                location.orientation.y, 
                location.orientation.z, 
                location.orientation.w]
    e = euler_from_quaternion(quaternion)
    O_z = e[2]'''
    O_z=location.orientation.z
                

def odom():
    rospy.init_node('odom', anonymous = True)
    rospy.Subscriber('/odom',Odometry, callback)

def deltaX(x):
    return abs(odom_x-x)
def deltaY(y):
    return abs(odom_y-y)
def deltaTheta(z):
    return abs(O_z-z)


#Todo: algorithm
       
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
kp=0.09
ka=0.2
kb=-0.3
def calc_gain_matrix(p,a,b):
    input_vector=numpy.array([p,a,b])

    gain_matrix=numpy.array([[kp,0,0],
                            [0,ka,kb]])
    robot_vals=numpy.matmul(gain_matrix,input_vector)
    print(robot_vals)
    return robot_vals



def cartesian_to_polar(x, y, t):
    #calculate r
    r = math.sqrt(x**2 + y**2)
    #calculate alpha
    alpha = -t+math.atan2(y, x)
    #calcualte beta
    beta=-(t+alpha)
    
    return r, alpha, beta
def build_transform (x,y,theta):

    cos = math.cos (math.radians(theta))
    sin = math.sin (math.radians(theta))
    cos = round (cos, 1)

    m1 = numpy.array([[cos,-sin,0,x],[sin,cos,0,y],[0,0,1,0],[0,0,0,1]])

    print (m1)
    return m1

def source_minus_odom(x,y,theta):
    return (odom_x-x,odom_y-y,O_z-theta)

def program():
  
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 100)
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

    while(p_a_b[0]>=0.05):
        print("dest coords are \n",goal_coords[0],"\n")
        dHs=build_transform(goal_coords[i][0],goal_coords[i][1],goal_coords[i][2])
        #dHs=build_transform(1,1,90)
        c_val=source_minus_odom(source_coords[i][0],source_coords[i][1],source_coords[i][2])
        print("Values from odom are x=",odom_x," y=",odom_y," theta=",O_z,"\n")
        print("Values from odom-source",c_val)
        
        cHs=build_transform(c_val[0],c_val[1],c_val[2])
        #cHs=build_transform(0,0,0)
        cHs_inv = numpy.linalg.inv(cHs)
        print("dHc is \n")
        dHc=numpy.matmul(cHs_inv,dHs)
        column_4 = dHc[0:3, 3]
        column_4_matrix = column_4.reshape(3, 1)
        rate.sleep()
        


    


        print(dHc)
        print("\n\n",column_4_matrix)
        theta=math.atan2(dHc[1][0],dHc[0][0])
        p_a_b=cartesian_to_polar(column_4_matrix[0],column_4_matrix[1],theta)
        print(p_a_b)
        

        u_w=calc_gain_matrix(p_a_b[0],p_a_b[1],p_a_b[2])
        twist_msg.linear.x = u_w[0]
        twist_msg.angular.z = u_w[1]
        rospy.loginfo(twist_msg)
        pub.publish(twist_msg)







      
    twist_msg.linear.x = 0
    twist_msg.angular.z = 0
    rospy.loginfo(twist_msg)
    pub.publish(twist_msg)




      
        #hello, this is a comment, 

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
        print("\n\n",column_4_matrix)

        p_a_b=cartesian_to_spherical(column_4_matrix[0],column_4_matrix[1],column_4_matrix[
        twist_msg.angular.z = 0.1
        rospy.loginfo(twist_msg)
        pub.publish(twist_msg)
        print('turn' + str(i))

        while(True):
            if not (abs(O_z-last_O_z) <= ((math.pi)*2)/sides):
                break
    '''
       
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

