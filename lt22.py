#!/usr/bin/env python

#To publish
import rospy
from geometry_msgs.msg import Twist

#To show the path
#from nav_msgs.msg import Path
import roslib
from nav_msgs.msg import Odometry
#from geometry_msgs.msg import PoseStamped

#To define the path
import matplotlib.pyplot as plt
import numpy as np
import math  #for sqrt
from math import degrees,atan2,radians 

import time 

def odometryCb(msg):
    global pos_x,pos_y,ori_z
    po =  msg.pose.pose
    pos_x = po.position.x
    pos_y = po.position.y
    ori_z =  po.orientation.z 

#getting points 
def path():
    a = 10
    t = np.arange(0, 2*(np.pi), 0.2) 

    x = math.sqrt(2)*np.cos(t)
    x = x/((np.sin(t)*np.sin(t)) + 1)
    x = x*a

    y = math.sqrt(2)*np.cos(t)*np.sin(t)
    y = y/((np.sin(t)*np.sin(t)) + 1)
    y = y*a

    #print x
    #print y
    plt.plot(x,y,'ro')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    #plt.show()
    return x,y


if __name__ == '__main__':
    try:             
        t = 0
        i = 0
        arrx = []
        arry = []
        xset = 0 
        ptx,pty = path()
                          
        rospy.init_node('lt', anonymous=True)
        vel_publisher = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        vel_msg = Twist()

        turn1_cmd = Twist()
        turn1_cmd.linear.x = 0
        turn1_cmd.angular.z = radians(45);


        turn2_cmd = Twist()
        turn2_cmd.linear.x = 0
        turn2_cmd.angular.z = -radians(45);

        r = rospy.Rate(30)
        while not rospy.is_shutdown():

            rospy.Subscriber('odom',Odometry,odometryCb)
            r.sleep()      #Note that it takes some time to subscribe and soo it is after sleep

            arrx.append(pos_x)
            arry.append(pos_y)          

            if ((pos_x - ptx[i])<0):
                xdir = 0.5
            else:
                xdir = -0.5

            if ((pos_y - pty[i])<0):
                ydir = 0.5
            else:
                ydir = -0.5

            print xdir,pos_x,ptx[i],ydir,pos_y,pty[i]

    
            if xset == 0:
                if (abs(pos_x-ptx[i])<0.05):
                    vel_msg.linear.x = 0
                    vel_msg.linear.y = 0
                    xset = 1
                    yset = 0
                    print "reached x point " 
                    print i

                    time.sleep(2)

                    r1 = rospy.Rate(5)
                    #turn 90
                    for x in range(0,10):
                        vel_publisher.publish(turn1_cmd)
                        r1.sleep()
                    print "Turned 90 degrees?"
                    time.sleep(2)

                else:
                    vel_msg.linear.x = xdir
                    vel_msg.linear.y = 0

            if xset == 1:
                    if (abs(pos_y-pty[i])<0.05):
                        vel_msg.linear.x = 0
                        vel_msg.linear.y = 0
                        yset = 1
                        print "reached y point "
                        print i 
                        time.sleep(2)

                        r1 = rospy.Rate(5)

                        #turn back 90
                        for x in range(0,10):
                            vel_publisher.publish(turn2_cmd)
                            r1.sleep()
                        xset = 0
                        time.sleep(2)
                        i = i+1
                        if i == 31:
                            print "done"
                            print arrx, arry
                            plt.plot(arrx,arry,'g^')
                            plt.show()
                            break

                    else:
                        vel_msg.linear.x = ydir
                        vel_msg.linear.y = 0  

# No movement in y diretion seen whatsoever.... shifting to yaw and move

            vel_msg.linear.z = 0
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            #vel_msg.angular.z = 0

            vel_publisher.publish(vel_msg)
            r.sleep()
        
    except rospy.ROSInterruptException:
        print "done"
        print arrx, arry
        plt.plot(arrx,arry,'g^')
        plt.show()
        pass




                   
