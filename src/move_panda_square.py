#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import time
from math import pi

from AR_week8_test.msg import square_size


def callback(data):
    # publishing initialised
    try:
        # Define starting robot configuration
        print '------------------- Received square size = %s -------------------' % data.size
        print '------------------- Going to Starting Configuration -------------------'
        start_conf = [0, -pi / 4, 0, -pi / 2, 0, pi / 3, 0]

        # Move Panda robot to starting configuration
        group.go(start_conf, wait=True)

        # stop() ensures that there is no residual movement
        group.stop()

        print '------------------- Planning Motion Trajectory -------------------'
        # initialise array of positions
        waypoints = []

        # get current group positions
        wpose = group.get_current_pose().pose

        wpose.position.y += data.size  # and sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.x += data.size  # Second move forward/backwards in (x)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.y -= data.size  # Third move sideways (y)
        waypoints.append(copy.deepcopy(wpose))

        wpose.position.x -= data.size  # Forth move forward/backwards in (x)
        waypoints.append(copy.deepcopy(wpose))

        (plan, fraction) = group.compute_cartesian_path(
            waypoints,  # waypoints to follow
            0.01,  # eef_step - cartesian translation, for Cartesian path interpolation at a resolution of 1 cm
            0.0)  # jump_threshold disabled

        # initialise the message for trajectory planning '/move_group/display_planned_path
        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = robot.get_current_state()
        display_trajectory.trajectory.append(plan)
        # publish the message to
        print '------------------- Showing Planned Trajectory -------------------'
        display_trajectory_publisher.publish(display_trajectory)

        time.sleep(5)
        # Execute planned trajectory
        print '------------------- Executing Planned Trajectory -------------------'
        group.execute(plan, wait=True)

    except rospy.ServiceException, e:
        print("Service call failed: %s" % e)


def move_panda_square():
    # initialise moveit commander
    moveit_commander.roscpp_initialize(sys.argv)

    # initialise new node
    rospy.init_node('move_panda_square', anonymous=True)

    # wait for service
    # subscribe to cubic_traj_params and send data to callback
    print '------------------- Waiting for square size -------------------'
    rospy.Subscriber('size', square_size, callback)
    # prevent from dying
    rospy.spin()


if __name__ == "__main__":
    # initialise robot commander
    robot = moveit_commander.RobotCommander()

    # initialise scene planning interface
    scene = moveit_commander.PlanningSceneInterface()

    # initialise move group commander
    group = moveit_commander.MoveGroupCommander('panda_arm')

    # initialise display trajectory publisher
    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                                   moveit_msgs.msg.DisplayTrajectory,
                                                   queue_size=0)
    move_panda_square()
