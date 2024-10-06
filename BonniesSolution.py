#!/usr/bin/env python3 
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
import math

x = 0.0
y = 0.0
theta = 0.0
goal_index = 0

# Define a list of goals
goals = [Point(5, 0, 0), Point(5, 5, 0), Point(0, 5, 0), Point(0, 0, 0)]

def newOdom(msg):
    global x, y, theta
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")
def Lspeed(xd,yd):
    return math.sqrt(math.pow(abs(xd-x),2) +   math.pow(abs(yd-y),2)        )


sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)

while not rospy.is_shutdown():
    goal = goals[goal_index]  # Get the current goal

    inc_x = goal.x - x
    inc_y = goal.y - y

    angle_to_goal = math.atan2(inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.1:
        speed.linear.x = 0.2
        speed.angular.z = (theta-angle_to_goal)*-1
    else:
        speed.linear.x = 0.3
        speed.angular.z = 0.0

    # Check if the robot has reached the goal (within a small threshold)
    if abs(inc_x) < 0.1 and abs(inc_y) < 0.1:
        rospy.loginfo(f"Reached goal {goal_index + 1}: {goal.x}, {goal.y}")  # Log the reached goal
        goal_index += 1  # Move to the next goal
        
        # Check if we reached the last goal
        if goal_index >= len(goals):  # If it is the last goal
            speed.linear.x = 0.0
            speed.angular.z = 0.0
            pub.publish(speed)  # Stop the robot
            rospy.signal_shutdown("Reached the last goal")  # Shutdown the node
            break  # Exit the loop

    pub.publish(speed)
    r.sleep()
