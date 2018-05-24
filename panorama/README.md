Terminal commands for panorama task

1. roslaunch rover_vision gscam.launch device:=/dev/video0
2. cd /opt/ros/kinetic/share/hugin_panorama
3. roslaunch hugin_panorama hugin_panorama.launch image:=/camera/image_raw
4. rosservice call /hugin_panorama/image_saver/save (Repeat this command to take another picture)
5. rosservice call / hugin_panorama /stitch (Will stitch all the pictures taken by the previous command)
6. xdg-open output.png
7. rosservice call /hugin_panorama/reset (Make sure to do this)
