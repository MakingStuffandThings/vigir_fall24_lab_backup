#!/usr/bin/env python3

from nav_msgs.msg import Odometry
import rospy
import tf
from geometry_msgs.msg import Twist 
import math
import numpy as np

import tf.transformations




#this is the callback function for the subscriber to take the information in odom and make them global variable to let other functions use
def callback(msg):
    #print(msg.pose.pose.position.x)
    global Odom_x 
    global Odom_y 
    global yaw 
    quaternion = (msg.pose.pose.orientation.x,
                  msg.pose.pose.orientation.y,
                  msg.pose.pose.orientation.z,
                  msg.pose.pose.orientation.w)
    euler = tf.transformations.euler_from_quaternion(quaternion)

    Odom_x = msg.pose.pose.position.x
    Odom_y = msg.pose.pose.position.y
    yaw = euler[2]
    
    #print(Odom_x , Odom_y, yaw)    
class cart:
    def __init__(self,x,y,theta):
        self.x = x
        self.y = y
        self.theta = theta
        self.vector = np.array([x,y,0,1])

    def abs(self):
        x = abs(self.x)
        y = abs(self.y)
        theta = self.theta
        return cart(x,y,theta)
    
    def print(self):
        print("X = " ,self.x , " y = " , self.y, " theta = ",math.degrees(self.theta) ,"\n")

    def __sub__(self,other):
        return cart(self.x - other.x,self.y - other.y, self.theta - other.theta)
    
    def __add__(self,other):
        return cart(self.x + other.x,self.y + other.y, self.theta + other.theta)
class pol:
    def __init__(self,rho,alpha,beta):
        self.rho = rho
        self.alpha = alpha 
        self.beta = beta
        self.vector = np.array([rho,alpha,beta])
    def speed(self, time):
        self.rho = self.rho/time 
        self.alpha = self.alpha/time
        self.beta = self.beta/time

    def print(self):
        print("rho :",self.rho,"\talpha: " , math.degrees(self.alpha), "\tbeta: ",math.degrees(self.beta) ,"\n" )

    def __sub__(self,other):
        return pol(self.rho - other.rho,self.alpha - other.alpha, self.beta - other.beta)
def cart_pol(cart):
    rho = math.sqrt((cart.x**2)+(cart.y**2))
    alpha = -cart.theta  + math.atan2(cart.y,cart.x)
    beta = -(cart.theta + alpha )
    return pol(rho,alpha,beta)

def transfomration_mat(change):
    #the rotation matrix 
    R_z = np.array([
        [np.cos(change.theta), -np.sin(change.theta), 0],
        [np.sin(change.theta),  np.cos(change.theta), 0],
        [0, 0, 1]
    ])
    # a 4x4 identity matrix 
    T = np.eye(4)
    #inserts to the top left 3x3
    T[:3,:3] = R_z
    T[:3, 3] = np.array([change.x, change.y, 0])
    return T    
def extract_cart(T):
    theta = math.atan2(T[1][0],T[0][0])
    x = T[0][3]
    y = T[1][3]
    return cart(x,y,theta)
def compute_cd_trasform(sd_transfrom,cs_transform):
    return np.matmul(np.linalg.inv(cs_transform),sd_transfrom)

def compute_vw(error):
    # for stability kp>0 , Ka-Kp > 0 , kb < 0 
    scale = 1

    Kp = 0.15 * scale
    Ka = 0.21 * scale
    Kb = -0.2 * scale
    
    v = error.rho * Kp 
    w = Ka*error.alpha + Kb *error.beta 
    return v,w
def move(goal):

    global Odom_x
    global Odom_y
    global yaw
    Odom_x=0.0
    Odom_y=0.0
    yaw=np.radians(0)

    pub = rospy.Publisher("/cmd_vel",Twist,queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    rospy.sleep(1)

    source_cart = cart(0,0,0)

    #source_cart.print()

    T = transfomration_mat(goal)
    old_cart = extract_cart(T)
    error_polar = cart_pol(old_cart) 
    motion = Twist()
    sd_transform = T
    motion.linear.x , motion.angular.z = compute_vw(error_polar)    
    pub.publish(motion)


    
    # error_cart = (cart(Odom_x,Odom_y,yaw) - source_cart).abs()

    # print(error_polar.rho)
    # print(error_polar.alpha)
    # print(error_polar.beta)
    # print(sd_transform)


    #while error_polar.rho > 0.01 and abs(error_polar.alpha) > math.radians(5) and abs(error_polar.beta) > math.radians(10):
    while error_polar.rho > 0.05 or abs(old_cart.theta) > math.radians(10) :
        rate.sleep()    

        error_cart = (cart(Odom_x,Odom_y,yaw) - source_cart)
        #error_cart.print()
        SC = transfomration_mat(error_cart)
        CD_transform = compute_cd_trasform(sd_transform,SC)
        old_cart = extract_cart(CD_transform)

        #old_cart.print()

        error_polar = cart_pol(old_cart)

        motion.linear.x , motion.angular.z = compute_vw(error_polar)

        pub.publish(motion)


        #print(SC)

        print("p :",error_polar.rho,"\talpha: " , math.degrees(error_polar.alpha), "\tbeta: ",math.degrees(error_polar.beta) ,"\n" )
      

        #if not error_polar.rho > 0.01 or not abs(error_polar.alpha) > math.radians(2) or not abs(error_polar.beta) > math.radians(2):
         #   print("TADA Im done")




    motion.linear.x = 0 
    motion.angular.z = 0
    pub.publish(motion)
    
    rate.sleep()

    print("not in while")








if __name__ == '__main__':
    try:
        rospy.init_node("poly" , anonymous=True)
        rospy.Subscriber("/odom", Odometry,queue_size=100,callback=callback)
        rospy.sleep(1)

        #test = cart(-0.5,1,(math.radians(90)))
        #move(test)



        location1 = cart(0.5,0.5,(math.radians(90)))
        move(location1)
        
        
        location2 = cart(-0.5,0.5,math.radians(180))
        move(location2)

        location3 = cart(-0.5,-0.5,math.radians(270))
        move(location3)
        
        location4 = cart(0.5,-0.5,math.radians(0))
        move(location4)


        rospy.spin()
        
    except rospy.ROSInterruptException:
        pass