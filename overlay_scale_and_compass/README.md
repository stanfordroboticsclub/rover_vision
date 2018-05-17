Terminal commands for overlaying scale and compass (hard-coded) on pano images

1. roslaunch image_overlay_scale_and_compass overlay.launch
2. roscd image_overlay_scale_and_compass/src/image_overlay
3. ./src/image_overlay_compass_and_scale/image_overlay.py --input-image [INSERT PATH TO IMAGE ITSELF] --heading 45 --scale-text 133 --output-file [DESIRED NAME OF PNG FILE TO BE SAVED IN SELF FOLDER]
