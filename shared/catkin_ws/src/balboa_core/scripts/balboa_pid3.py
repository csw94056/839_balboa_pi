#!/usr/bin/env python
from os import kill
import struct
import serial
import sys
import math
import rospy
from std_msgs.msg import UInt8
from std_msgs.msg import Int16
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from balboa_core.msg import balboaLL
from balboa_core.msg import balboaMotorSpeeds
from balboa_core.msg import lineSensor
from ball_detector.msg import ballLocation
from landmark_self_sim.msg import landmarkLocation

INF = 100000000000

class PIDNode(object):
    '''Class to control the balboa robot based on PID controllers'''
    # Sung Woo Choi and Karissa Jelonek
    
    def __init__(self):
        # Initiate ros node /balboa_pid
        rospy.init_node('balboa_pid')
        
        # Initiate Subscribers
        self.sub_TurtleTeleopKey = rospy.Subscriber('turtle1/cmd_vel_pid', Twist, self.handleTurtleTeleopKey)
        self.sub_BalboaLL = rospy.Subscriber('balboaLL', balboaLL, self.handleBalboaLL)
        #self.sub_ballLocationGreen = rospy.Subscriber('/g/ballLocation', ballLocation, self.handleBallLocationGreen)
        self.sub_ballLocationPurple = rospy.Subscriber('/p/ballLocation', ballLocation, self.handleBallLocationPurple)
        self.sub_ballLocationYellow = rospy.Subscriber('/y/ballLocation', ballLocation, self.handleBallLocationYellow)
        self.sub_LandmarkLocation = rospy.Subscriber('/landmarkLocation', landmarkLocation, self.handleLandmarkLocation)
        #self.sub_ballLocation = rospy.Subscriber('ballLocation', ballLocation, self.handleBallLocation)
        self.sub_ls = rospy.Subscriber('lineSensor', lineSensor, self.handleLineSensor)
        self.sub_ir = rospy.Subscriber('irRange', Float64, self.handleIrRangeSensor)
        self.pub_ls = rospy.Publisher('lineSensorMap', lineSensor, queue_size=10)
        # Initiate Publishers
        self.pub_distancePID = rospy.Publisher('distancePID', balboaMotorSpeeds, queue_size=10)
        self.pub_angularPID = rospy.Publisher('angularPID', Int16, queue_size=10)
        self.pub_servo_distance = rospy.Publisher('servoDistance', Float64, queue_size=10)
        self.activate_angleVelPID = 0
        # Initiate variables for current measurements
        self.current_angle = 0
        self.current_distance = 0        
        # Initiate target values for pid_control()
        self.target_distance = INF
        self.target_angle = INF
        # Initiate variables used for pid_control()
        self.prev_error_distance = 0
        self.prev_error_angle = 0
        self.integral_distance = 0
        self.integral_angle = 0
        # ROS Parameter Server
        # set PID parameters to receive settings from launch file
        rospy.set_param('distanceCtrl/P', 0.013)
        rospy.set_param('distanceCtrl/I', 0.0)
        rospy.set_param('distanceCtrl/D', 0.002)
        rospy.set_param('angleCtrl/P', 1.0)
        rospy.set_param('angleCtrl/I', 0.0)
        rospy.set_param('angleCtrl/D', 0.1)
        rospy.set_param('clean_angleCtrl/P', 0.13)
        rospy.set_param('clean_angleCtrl/I', 0.0)
        rospy.set_param('clean_angleCtrl/D', 0.0)
        self.draw_CS = 0
        self.angle_speed_limit = 10
        self.distance_speed_limit = 15
        # flag for reactive control
        self.reactive_control = 0
        self.r_ctrl_dist_target = 0
        #lineSensor values
        self.sensor0 = 2500
        self.sensor1 = 2500
        self.sensor2 = 2500
        self.sensor3 = 2500
        self.sensor4 = 2500

        #balboaLL variables
        self.angleX = 0
        self.angleY = 0  # unit: degrees
        
        self.bugFlag = 0
        self.unobsMoveAngle = 0

        #flag for ball detector
        self.ball_detector = 0
        #fixed distance variable for the robot to keep from the target ball
        self.ball_detector_dist = 0

        #flag for pac-man
        self.pac_man = 0
        #the ball is detected
        self.ball_detected = 0
        self.ball_detector = 0
        
        #flag for landmark detector
        self.landmark_detector = 0
        self.landmark_num = 0

        self.angleCorrection = 1
        self.test_states = 0

        self.y_ball_found = 0

    def handleTurtleTeleopKey(self, teleop_msg):
        # update target distance and angle based on turtle_teleop_key/cmd_vel
        if teleop_msg.linear.x == 0:
            self.target_distance = INF
        else:
            if self.target_distance == INF:
                self.target_distance = self.current_distance + (teleop_msg.linear.x / 2.0)*1566.0
            else:
                self.target_distance = self.target_distance + (teleop_msg.linear.x / 2.0)*1566.0
                
        if teleop_msg.angular.z == 0:
            self.target_angle = INF
            angularPID_msg = Int16()
            angularPID_msg.data = 0
            self.pub_angularPID.publish(angularPID_msg)
        else:
            if self.target_angle == INF:
                self.target_angle = self.current_angle + (teleop_msg.angular.z / 2.0)*90.0    # unit: degrees
            else:
                self.target_angle = self.target_angle + (teleop_msg.angular.z / 2.0)*90.0

    def handleLandmarkLocation(self, lm_msg):
        if self.landmark_detector == 0 or abs(lm_msg.code) == 1:
            return
        if lm_msg.code != self.landmark_num:
            return

        print("LandMark--------------------")

        #distance = 304.89e^(-0.006 * height)
        #distance = 304.89 * math.exp(-0.006 * lm_msg.height) * math.cos(self.angleY*math.pi/180.0) #cm
        distance = 304.89 * math.exp(-0.006 * lm_msg.height)  #cm

        xmax = 650 #maximum of xtop and xbotton of landmarkLocation
        
        # x_avg is the mean of xtop and xbottom
        x_avg = (lm_msg.xtop + lm_msg.xbottom)/2.0
        # detected landmark image width; computed based on the height of landmark image
        img_width = lm_msg.height * 1.29
        # shifting x_avg to the center of the camera
        x_0 = x_avg - xmax / 2
        # radius is half of the landmark image width
        radius = img_width / 2.0
        # rescale x_0 in respect to radius to prevent over-turning due to large angle
        x = x_0 * radius / xmax 

        print("distance ", distance)
        print("radius ", radius)
        print("angle ",  (math.atan(x/distance) * 180.0/math.pi))
        print("x_0 ", x_0)
        dist_ctrl = 1

        angle_ = (math.atan(x/distance) * 180.0/math.pi)
        # if x is larger than radius, the robot will turn to face the landmark
        if (abs(x_0) > radius):
            print("angle control ----------------- ball detector")
            #angle_ = (math.atan(x/distance) * 180.0/math.pi)
            
            # if the robot is close to the landmark, we reduce angle control by half to prevernt overshoot in angle turn
            if radius > 180:
                angle_ = 0.5 * angle_

            print("angle_ ", angle_)
            self.target_angle = self.current_angle - angle_ * self.angleCorrection
            dist_ctrl = 0
            
        # if robot is facing the landmark, distance control is allowed to control the robot to move forward and backward
        if abs(self.lm_dist - distance) > 15 and dist_ctrl == 1:
            print("distance control ---------------ball detector")

            if distance > self.lm_dist:
                self.target_distance = self.current_distance + (distance - self.lm_dist) * 52.2
                self.target_angle = INF

        # if the robot is close enough to detect the ball infront of the landmark, ball_detector function is activate to hit the ball
        if distance <= self.lm_dist + 10 and dist_ctrl == 1:    
            # First, the robot will keep 90 cm away from the target ball and then it will move forward to hit the ball
            self.ball_detector_dist = 90
            self.ball_detector = 1
            self.pac_man = 1
            self.landmark_detector = 0
            self.pac_man_ctrl_enabled = 0
            self.target_distance = INF
            self.target_angle = INF

        #print("code ", lm_msg.code)
        #print("xtop ", lm_msg.xtop, " ytop ", lm_msg.ytop, " xbottom ", lm_msg.xbottom, " ybotton ", lm_msg.ybottom )
        #print("height ", lm_msg.height)
        #lm_width = lm_msg.height * 1.29
        #print("width ", lm_width)
        
    def handleBallLocationGreen(self, bl_msg):
        if self.ball_detector == 0 or bl_msg.radius < 25:
            return
        print("green ball")
        dist = 189.23 * math.exp(-0.014 * bl_msg.radius) # cm
        if dist < 45:
            self.test_states = 2

    def handleBallLocationPurple(self, bl_msg):
        if self.ball_detector == 0 or  bl_msg.radius < 25:
            return
        print("purple ball")
        dist = 189.23 * math.exp(-0.014 * bl_msg.radius) # cm
        if dist < 45:
            self.test_states = 2

    def handleBallLocationYellow(self, bl_msg):
        if self.ball_detector == 0 or bl_msg.radius < 25:
            return
        print("yellow ball")
        # self.y_ball_found = 1
        self.ballLocation(bl_msg)
        
    def ballLocation(self, bl_msg):
        # ignore if ball detector is not activate or radius is less than 25
        if self.ball_detector == 0 or bl_msg.radius < 25:
            return

        self.y_ball_found = 1
        
        #if self.pac_man_ctrl_enabled > 0:
        #    return
        
        #dist = 189.23 * math.exp(-0.014 * bl_msg.radius) * math.cos(self.angleY * math.pi / 180.0) # cm
       # dist = 189.23 * math.exp(-0.014 * bl_msg.radius) * math.cos(self.angleY * math.pi / 180.0) # cm
        dist = 189.23 * math.exp(-0.014 * bl_msg.radius) # cm
        # scale x variable in respect to the scale of the radius from ballLocation
        x = bl_msg.x * bl_msg.radius / bl_msg.imageWidth
        
        #print("bl_msg.x ", bl_msg.x)
        print("x ", x)
        print("dist ", dist)
        print("angle ",  ((math.atan(x / dist)) * 180.0 / math.pi) )
        print("radius ", bl_msg.radius)
        print("bl_msg.x ", bl_msg.x)
        print("range ", abs(self.ball_detector_dist - dist))

        angle_ = ((math.atan(x/dist)) * 180.0 / math.pi)
        # position the robot to face the ball straight on
        #if abs(bl_msg.x) > bl_msg.radius or abs(angle_) > 5:
        if abs(angle_) > 5:
            print("\n angle control---------------------")
            # if the robot is close to the ball, then reduce angle control by half
            #if bl_msg.radius > 50:
            if dist <= 50:
                angle_ = 0.8 * angle_
                
            self.target_angle = self.current_angle - angle_
            self.target_distance = INF
            return

        # move the robot toward the ball
        elif abs(self.ball_detector_dist - dist) > 5:
            print("\n distance control---------------------")
            self.target_distance = self.current_distance + (dist - self.ball_detector_dist) * 52.2
            self.target_angle = INF
            return
            
        #servo_msg = Float64()
        #servo_msg.data = dist
        #self.pub_servo_distance.publish(servo_msg)

        if self.pac_man == 0:
            return

        print("\npac-man---------------------ctrl-------------")
        print("dist: ", dist)
        print("self.ball_detector_dist: ", self.ball_detector_dist) 
        # move the robot to hit the ball; addition forward 3 cm movement
        #if dist < self.ball_detector_dist + 10:
            #self.pac_man_ctrl_enabled = 1
        print("pacman ctrl----------------------------------")
            #self.target_distance += (self.ball_detector_dist + 3) * 52.2
        self.target_distance = self.current_distance + (dist + 5) * 52.2
        self.target_angle = INF
        print("target_distance ", self.target_distance)
        print("current_distance ", self.current_distance)
        # set ball_detector to 0 to give robot time to hit the ball
        self.ball_detector = 0

    def handleBalboaLL(self, balboall_msg):               
        # receive PID settings from launch file or command line via (rosparam set param_name value)
        self.Kp_distance = rospy.get_param('distanceCtrl/P')
        self.Ki_distance = rospy.get_param('distanceCtrl/I')
        self.Kd_distance = rospy.get_param('distanceCtrl/D')
        if self.activate_angleVelPID == 1:
            self.Kp_angle = rospy.get_param('angleCtrl/P')
            self.Ki_angle = rospy.get_param('angleCtrl/I')
            self.Kd_angle = rospy.get_param('angleCtrl/D')
        else:
            self.Kp_angle = rospy.get_param('clean_angleCtrl/P')
            self.Ki_angle = rospy.get_param('clean_angleCtrl/I')
            self.Kd_angle = rospy.get_param('clean_angleCtrl/D')

        # if no yellow ball is found then increment from 1 to 6 each iteration
        if self.y_ball_found > 0:
            self.y_ball_found = self.y_ball_found + 1
            # if not yellow ball is found for 5 increment set to 0 (no yellow ball visible)
            if self.y_ball_found == 20:
                self.y_ball_found = 0

        # self.ball_detector only set to 0 if the robot tried to hit the ball
        # we wait for self.y_ball_found increment to 6 and set back to 0 to provide sufficient enough time for the robot to hit the ball
        if self.y_ball_found == 0 and self.ball_detector == 0 and self.test_states > 0:    
            self.ball_detector = 1

        self.angleY = balboall_msg.angleY / 1000.0 #in degree
        self.angleX = balboall_msg.angleX
        self.current_angle = balboall_msg.angleX / 1000.0 # balboall_msg.angleX is in millidegrees
        self.current_distance = balboall_msg.distanceLeft * 1.0
        
        self.tangent_bug_states(balboall_msg)
        #print("cd ", self.current_distance, " td ", self.target_distance)
        #print("ca ", self.current_angle, " ta ", self.target_angle)
        # distancePID
        if self.target_distance < INF:
            r_distance, self.prev_error_distance, self.integral_distance = self.pid_control(self.Kp_distance, self.Ki_distance, self.Kd_distance, self.target_distance, self.current_distance, self.prev_error_distance, self.integral_distance)
            # limits the motor speed to prevent the robot falling over
            if r_distance > self.distance_speed_limit:
                r_distance = self.distance_speed_limit
            if r_distance < -self.distance_speed_limit:
                r_distance = -self.distance_speed_limit
            # pubhlish distancePID node message 
            distancePID_msg = balboaMotorSpeeds()
            distancePID_msg.left = int(r_distance)
            distancePID_msg.right = int(r_distance)
            self.pub_distancePID.publish(distancePID_msg)
            
        # anglePID
        if self.target_angle < INF:
            r_angle, self.prev_error_angle, self.integral_angle = self.pid_control(self.Kp_angle, self.Ki_angle, self.Kd_angle, self.target_angle, self.current_angle, self.prev_error_angle, self.integral_angle)
            # limits the motor speed to prevent the robot falling over
            if r_angle > self.angle_speed_limit:
                r_angle = self.angle_speed_limit
            if r_angle < -self.angle_speed_limit:
                r_angle = -self.angle_speed_limit
            if self.activate_angleVelPID == 1:
                # publish anglePID node message
                angularPID_msg = Int16()
                angularPID_msg.data = int(r_angle)
                self.pub_angularPID.publish(angularPID_msg)
            else:
                # pubhlish distancePID node message to rotate 
                distancePID_msg = balboaMotorSpeeds()
                distancePID_msg.left = int(-r_angle)
                distancePID_msg.right = int(r_angle)
                self.pub_distancePID.publish(distancePID_msg)
            
    def handleIrRangeSensor(self, ir_msg):
        if self.y_ball_found > 0:
            self.test_states = 1
            return
        
        if self.reactive_control > 0:
            # the robot follows if there is a distance between target and sensed data
            # if the sensed data is father than 50 cm, then the robot will not follow
            if self.test_states > 0:
                self.test_states_movement(ir_msg);
                
            elif abs(ir_msg.data - self.r_ctrl_dist_target) > 0 and abs(ir_msg.data - self.r_ctrl_dist_target) <= 160:
                #self.target_distance = self.current_distance + ((ir_msg.data - self.r_ctrl_dist_target) * math.cos(self.angleY) * 52.2)
                self.target_distance = self.current_distance + ((ir_msg.data - self.r_ctrl_dist_target) * 52.2)
                # target distance of 52.2 moves Balboa 1 cm

    def test_states_movement(self, ir_msg):
        # state 1: move forward until object is detected. keep 20 cm away from the object.
        if self.test_states == 1:
            self.target_distance = INF - 1
            self.target_angle = INF
            if abs(ir_msg.data) <= self.r_ctrl_dist_target + 2:
                # the robot is 20cm away from the object
                self.target_distance = INF
                self.set_motorSpeed(0, 0)
                self.test_states = 2
                print("test state 2")

        # state 2: rotate 90 degree to the right.
        elif self.test_states == 2:
            if self.target_angle == INF:
                self.target_angle = self.current_angle - 90.0
                self.target_distance = INF
                
            if abs(self.target_angle - self.current_angle) <= 5:
                # the robot rotated 90 +- 5 degree
                self.target_angle = INF
                self.set_motorSpeed(0, 0)
                self.test_states = 1
                print("test state 1")

    def set_motorSpeed(self, left, right):
        speed_msg = balboaMotorSpeeds()
        speed_msg.left = int(left)
        speed_msg.right = int(right)
        self.pub_distancePID.publish(speed_msg)


    def main_loop(self):
        r = rospy.Rate(200)
        set_distance = 2600
        set_angle = -90
        while not rospy.is_shutdown():
            
            # terminal-based control
            # i.e. a10 means rotate 10 degree in right turn
            # i.e. d-1566 means move backward (1566*9.89478) / 1292 = 12 inch
            # i.e. v30 means rotate 30 degree/s in right turn
            val = raw_input("Enter target value: ")
            if val[0] == 'q':
                # terminate all controls
                self.target_distance = self.current_distance
                self.target_angle = INF
                self.reactive_control = 0
                self.bugFlag = 0
                self.r_ctrl_dist_target = 0
                self.landmark_detector
                self.ball_detector = 0
                self.ball_detector_dist = 0
                self.pac_man = 0
                self.test_states = 0
                
            elif val[0] == 'a' and val[1] == 'v' and val[2] == 'a':
                # activate angleVelPID
                self.activate_angleVelPID = 1
                
            elif val[0] == 'a' and val[1] == 'v' and val[2] == 'd':
                # deactivate angleVelPID 
                self.activate_angleVelPID = 0
                
            elif val[0] == 'a':
                # set target angle
                self.reactive_control = 0
                self.target_distance = INF
                self.target_angle = self.current_angle + int(val[1:])       # unit: degree
                
            elif val[0] == 'd':
                # set target distance
                self.reactive_control = 0
                self.target_angle = INF
                self.target_distance = self.current_distance + 125* int(val[1:])     # unit: inch
            
            elif val[0] == 'v':
                # set target angular velocity
                self.reactive_control = 0
                self.target_angle = INF
                self.target_distance = INF
                # publish anglePID
                angularPID_msg = Int16()
                angularPID_msg.data = int(val[1:])
                self.pub_angularPID.publish(angularPID_msg)
                
            elif val[0] == 'l' and val[1] == 'm':
                self.landmark_num = int(val[2:])
                self.landmark_detector = 1
                self.lm_dist = 110
                self.pac_man_ctrl_enabled = 0
                self.target_angle = INF
                self.target_distance = INF
                print("------------------------landmark launched")
                # while self.searching == 1:
                    # print("spinning to find landmark-----------------------")
                    #rospy.sleep(1)
                    # self.target_angle = self.current_angle + 15 * self.angleCorrection

            elif val[0] == 'p' and val[1] == 'a' and val[2] == 'c':
                self.ball_detector_dist = 50
                self.ball_detector = 1
                self.pac_man = 1
                self.target_angle = INF
                self.target_distance = INF

            elif val[0] == 't' and val[1] == 'e' and val[2] == 's' and val[3] == 't':
                self.reactive_control = 1
                # distance to maintain from object
                self.r_ctrl_dist_target = 30
                self.test_states = 1
                self.ball_detector_dist = 50
                self.ball_detector = 1
                self.pac_man = 1
                self.target_angle = INF
                self.target_distance = INF
                print("r_ctrl ", self.r_ctrl_dist_target)
                print("test state 1")


            elif val[0] == 'b' and val[1] == 'd':
                self.ball_detector_dist = int(val[2:])
                self.ball_detector = 1
                self.target_angle = INF
                self.target_distance = INF
                
            elif val[0] == 'i' and val[1] == 'r':
                # IR sensor range is 20-150cm
                #if int(val[2:]) > 19 and int(val[2:]) < 51:
                if int(val[2:]) > 4 and int(val[2:]) < 151:
                    self.reactive_control = 1
                    # distance to maintain from object
                    self.r_ctrl_dist_target = int(val[2:])
                    print("r_ctrl ", self.r_ctrl_dist_target)
                    
            elif val[0] == 't' and val[1] == 'b':
                self.bugFlag = 1
                self.distanceFromObs = 30
                self.initPosAngle = 0
                self.target_distance = INF
                self.target_angle = INF

            r.sleep()
            
    def pid_control(self, Kp, Ki, Kd, target, current_val, prev_error, integral):
        '''
            r = rotation
            e_current (e_i) = error of current time step
            e_prev (e_(i-1)) = error of previous time step
            a_t = target parameter
            a_i = current parameter 
            e_current = a_t(i) - a_i(i)
            e_prev = a_t(i-1) - a_i(i-1)
            integral(i) = integral(i-1) + (a_t - a_i)
            control: r = Kp*(a_t - a_i) + Kd*(e_current - e_prev) + Ki*integral
        '''
        error = target - current_val
        delta_error = error - prev_error
        integral += error
        r = Kp*error + Ki*integral + Kd*delta_error
        return r, error, integral
        
    def handleLineSensor(self, ls_msg):
        self.sensor0 = ls_msg.sensor0
        self.sensor1 = ls_msg.sensor1
        self.sensor2 = ls_msg.sensor2
        self.sensor3 = ls_msg.sensor3
        self.sensor4 = ls_msg.sensor4
            
    def tangent_bug_states(self, balboall_msg):
        if self.bugFlag > 0:
            tangentBug_msg = balboaMotorSpeeds()
            self.angle_speed_limit = 4
            
            # move forward at fixed speed
            if self.bugFlag == 1:
                self.initPosAngle = self.current_angle
                self.startingTBAngle = self.current_angle
                self.totalTravelDist_x = 0      # forward distance
                self.totalTravelDist_y = 0      # left/right distance
                tangentBug_msg.left = int(10)
                tangentBug_msg.right = int(10)
                self.pub_distancePID.publish(tangentBug_msg)
                print("startingTBAngle ", self.startingTBAngle, " ir ", self.ir)
                    
                # obstacle detected winthin 50 cm
                if self.ir < 50:
                    tangentBug_msg.left = int(0)
                    tangentBug_msg.right = int(0)
                    self.pub_distancePID.publish(tangentBug_msg)
                    self.unobstructedAngleRight = 0
                    self.unobstructedAngleLeft = 0
                    self.reactive_control = 1
                    self.r_ctrl_dist_target = 30
                    # distance between obstacle and the robot is 30 +/- 0.5 cm
                    if abs(self.ir - self.distanceFromObs) <= 0.5:
                        self.bugFlag = 2
                        self.reactive_control = 0
                        print("bug flag 2")
                        
            # search for nearest unobstructed angle to left
            if self.bugFlag == 2:
                self.target_angle = INF
                self.target_distance = INF
                angleScan_msg = Int16()
                angleScan_msg.data = int(10)
                self.pub_angularPID.publish(angleScan_msg)
                
                if self.ir <= 50:
                    self.distanceToBoundaryLeft = self.ir
                else:
                    self.unobstructedAngleLeft = self.current_angle
                    print("self.unobstructedAngleLeft ", self.unobstructedAngleLeft)
                    self.angle_speed_limit = 4
                    self.bugFlag = 3
                    print("bug flag 3")
                    
            # return to startingTBAngle (initial angle position)
            if self.bugFlag == 3:
                # self.target_angle = self.startingTBAngle 
                self.target_angle = self.current_angle - abs(self.unobstructedAngleLeft - self.startingTBAngle)
                print("target_angle: ", self.target_angle)
                if self.current_angle < self.startingTBAngle:
                # if abs(self.current_angle - self.startingTBAngle) <= 1:
                    angleScan_msg = Int16()
                    angleScan_msg.data = int(0)
                    self.pub_angularPID.publish(angleScan_msg)
                    self.bugFlag = 4
                    print("bug flag 4")
                
            # search for nearest unobstructed angle to the right
            if self.bugFlag == 4:
                self.target_angle = INF
                self.target_distance = INF
                angleScan_msg = Int16()
                angleScan_msg.data = int(-10)
                self.pub_angularPID.publish(angleScan_msg)
                
                if self.ir <= 50:
                    self.distanceToBoundaryRight = self.ir
                else:
                    self.unobstructedAngleRight = self.current_angle
                    print("self.unobstructedAngleRight ", self.unobstructedAngleRight)
                    self.target_angle = self.startingTBAngle
                    self.bugFlag = 5
                    print("bug flag 5")
              
            # return to startingTBAngle (initial angle position)
            if self.bugFlag == 5:
                self.target_angle = self.current_angle + abs(self.unobstructedAngleRight - self.startingTBAngle)
                print("target_angle: ", self.target_angle)
                if self.current_angle > self.startingTBAngle:
                    angleScan_msg = Int16()
                    angleScan_msg.data = int(0)
                    self.pub_angularPID.publish(angleScan_msg)
                    self.target_distance = INF
                    self.target_angle = INF
                    self.unobsMoveAngle = 0
                    self.bugFlag = 6
                    print("bug flag 6")
                        
            # turn in direction of furthest unobstructed angle
            if self.bugFlag == 6:
                if self.unobsMoveAngle == 0:
                    if abs(self.startingTBAngle - self.unobstructedAngleRight) < abs(self.startingTBAngle - self.unobstructedAngleLeft):
                        # decrease angle by 25 degrees to move away from the object
                        self.unobsMoveAngle = -abs(self.startingTBAngle - self.unobstructedAngleRight) - 25
                        self.target_angle = self.current_angle + self.unobsMoveAngle
                    else:
                        # increase angle by 25 degrees to move away from the object
                        self.unobsMoveAngle = abs(self.startingTBAngle - self.unobstructedAngleLeft) + 25
                        self.target_angle = self.current_angle + self.unobsMoveAngle
                print("ta ", self.target_angle, " ual ", self.unobstructedAngleLeft, " ca ", balboall_msg.angleX / 1000)
                    
                if abs(self.current_angle - self.target_angle) <= 1:
                    self.target_angle = INF
                    self.target_distance = INF
                    
                    # move 6 cm futher in x and y direction
                    self.moveX = (self.distanceFromObs + 6)
                    self.moveY = (self.distanceFromObs + 6) * math.sin(self.unobsMoveAngle * math.pi / 180.0)
                    self.target_distance = self.current_distance + math.sqrt(self.moveX**2 + self.moveY**2) * 52.2
                    self.bugFlag = 7
                    print("bug flag 7")
            
            # wait until the robot move forward the alpha (the distance of between the object and the robot plus 6 * sqrt(2))
            if self.bugFlag == 7:
                if (self.target_distance - self.current_distance) <= 1:
                    self.target_angle = INF
                    self.target_distance = INF
                    self.target_angle = self.current_angle - self.unobsMoveAngle
                    self.bugFlag = 8
                    print("bug flag 8")
                
            # wait until the robot rotate to unobstructed angle
            if self.bugFlag == 8:
                if abs(self.current_angle - self.target_angle) <= 1:
                    self.target_angle = INF
                    self.target_distance = INF
                    self.target_distance = self.current_distance + 30 * 52.2
                    self.bugFlag = 9
                    print("bug flag 9")

            # wait until the robot move 30 cm forward
            if self.bugFlag == 9:
                if (self.target_distance - self.current_distance) <= 1:
                    self.target_angle = INF
                    self.target_distance = INF
                    self.target_angle = self.current_angle - self.unobsMoveAngle
                    self.bugFlag = 10
                    print("bug flag 10")
            
            # wait until the robot rotate to perpendicular of unobstructed angle
            if self.bugFlag == 10:
                if abs(self.current_angle - self.target_angle) <= 1:
                    self.target_angle = INF
                    self.target_distance = INF
                    self.target_distance = self.current_distance + math.sqrt(self.moveX**2 + self.moveY**2) * 52.2
                    self.bugFlag = 11
                    print("bug flag 11")
            
            # wait until the robot move forward the distance alpha (the distance of between the object and the robot plus 6 * sqrt(2)) to come back to the orignal trajectory
            if self.bugFlag == 11:
                if (self.target_distance - self.current_distance) <= 1:
                    self.target_angle = INF
                    self.target_distance = INF
                    self.target_angle = self.current_angle + self.unobsMoveAngle
                    self.bugFlag = 12
                    print("bug flag 12")
            
            # wait until the robot rotated to back to the original angular position of the original trajectory
            if self.bugFlag == 12:
                if abs(self.current_angle - self.target_angle) <= 1:
                    self.target_angle = INF
                    self.target_distance = INF
                    self.reactive_control = 0
                    self.bugFlag = 1
                    print("bug flag 1")
        
            
if __name__ == '__main__':
    pid = PIDNode()
    pid.main_loop()
 
