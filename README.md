This ROS package automatically generates Cartesian space movements of the end-effector of the Panda robot manipulator: the end-effector "draws" squares of different sizes on the x-y Cartesian plane, starting from a given robot configuration.
In order to run the package, extract the package into your catkin workspace and ensure you have MoveIt installed.
    First we need to download 2 repositories, which will allow to start rViz with the Panda robot model

    From your catkin workspace, run the following lines of code in order to download 2 repositories, which will allow you to start Rviz with the Panda robot model:

    git clone -b kinetic-devel https://github.com/ros-planning/moveit_tutorials.git
    git clone -b kinetic-devel https://github.com/ros-planning/panda_moveit_config.git

    In order to make all of the nodes executable, run the following comands from the "scripts" folder containing all the nodes

    chmod +x square_size_generator.py
    chmod +x move_panda_square.py

    First we need to get roscore running:

    roscore

    In a separate terminal we can now launch the Rviz by running:

    roslaunch panda_moveit_config demo.launch

    In another terminal run the following:

    rosrun AR_week8_test square_size_generator.py

    This will initiate the first node, which generates a random square size and publishes it to the 'size' topic

    In a seperate terminal run the following:

    rosrun AR_week8_test move_panda_square.py

    This will initiate our main node, which subscribes to the 'size' topic, and communicates with the Panda Arm through MoveIt to 'draw' squares on a Cartesian plane

    To visulise the the joints positions, run: (add joint state positions 0-6 topics in the GUI)

    rosrun rqt_plot rqt_plot

