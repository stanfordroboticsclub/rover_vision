Terminal commands for panorama task

1. roslaunch rover_vision gscam.launch device:=/dev/video0
    1. (cd /opt/ros/kinetic/share/hugin_panorama)
2. roslaunch hugin_panorama hugin_panorama.launch image:=/camera/image_raw
3. rosservice call /hugin_panorama/image_saver/save
4. rosservice call / hugin_panorama /stitch
5. xdg-open output.png
6. rosservice call /hugin_panorama/reset
