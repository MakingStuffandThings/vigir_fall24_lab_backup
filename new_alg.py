#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry 
import numpy

import math
from  tf.transformations import euler_from_quaternion

goals=4
length=0.5

theta_tol=0.01
dest_tol=0.01
k=0.08
l=1



goal_coords=[(2,1,math.pi),(0,0,math.pi),(1,0,((math.pi)/2)*3),(1,2,0)]


def callback(data):
    global odom_x,odom_y,O_z
    location = data.pose.pose
    odom_x = location.position.x
    odom_y = location.position.y
    quaternion = [location.orientation.x, #this gives us converts the odom data to radians
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
def deltaY(y):  y: 0.0
    return abs(odom_y-y)
def deltaTheta(z):
    return abs(O_z-z)



def linear_speed(dist):#this function allows for a slowdown in speed as you reach a target distance
    return (dist/2)*k
def theta_speed(dist):#this function allows for a slowdown in speed as you reach a target theta
    return (dist/2)*l 
def dest(dest_X,dest_y):
    return math.sqrt( math.pow(abs(odom_x-dest_X),2) + math.pow(abs(odom_y-dest_y),2) )

def theta_starting(xd,yd):
    #hyp=dest(xd,yd)
    adj=abs(odom_x-xd)
    opp=abs(odom_y-yd)

    return math.atan(opp/adj) #this gives us the theta angle that points to the destination, we will want to check out O_z to
#make sure it is as close to this value as possible when we are traveling and before we start




def program():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size =  y: 0.0
 1000)
    rospy.sleep(2)
    i = 0
    

#this is an example twist msg
#        twist_msg.linear.x = 0.1
#        twist_msg.angular.z = 0.0
#        rospy.loginfo(twist_msg)
#        pub.publish(twist_msg)



  y: 0.0

    while(i < goals):
        i = i + 1
        last_x = odom_x
        last_y = odom_y
        last_O_z = O_z
        xd=goal_coords[i][1]
        yd=goal_coords[i][2]
        twist_msg = Twist()
        
        C_dest=dest(xd,yd)#calc dest, and theta_starting
        Starting_theta=theta_starting(xd,yd)
        
        print("Current distance is ",C_dest,"\nStarting Theta is ",Starting_theta)


            #rotate to theta_starting
        while(  abs(O_z-Starting_theta) >=theta_tol ):
            twist_msg.linear.x=0
            twist_msg.angular.z=theta_speed(abs(O_z-Starting_theta))   
            pub.publish(twist_msg)
        print("Current robot theta is ",O_z)    

        


        twist_msg.linear.x=0 #stop the robot
        twist_msg.angular.z=0   
        pub.publish(twist_msg)
        
        print("Stopping the robot")
        rospy.sleep(1)

        print("Moving forward")

        print("Proposed Linear speed ",linear_speed(dest(xd,yd)),"\n")
        input("Press any key to continue")


        while(C_dest>=dest_tol):
            twist_msg.linear.x=linear_speed(dest(xd,yd)) #send it
            twist_msg.angular.z=0   
            pub.publish(twist_msg)
        
        print("Stopping the robot")
        twist_msg.linear.x=0 #stop the robot
        twist_msg.angular.z=0   
        pub.publish(twist_msg)
        print("Current x ",odom_x,"\nCurrent y",odom_y)
        print("Goal x ",xd,"\nGoal y ",yd)


        return


        #pub linear_speed pub theta_speed
        #while(dest<=des_tol)
            #dest_calc()
            #pub(linear_speed)
        #rotate to desired goal theta





    
    
    
    
    
    
    return



if __name__ == '__main__':
    try:
        odom()
        rospy.sleep(1)
        program()
    except rospy.ROSInterruptException:
        print('exception')
        pass

