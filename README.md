this project was started as a way to continuously monitor the built-in webcam and a couple of connected webcams simultaneously for any movements. When any movement is detected in any of the cameras being monitored, these frames are saved and written to a numpy array.

The script was initially written to output to video directly, but I ran into situations where there were very few frames that were recorded (because there was very little movement) and that led to very short videos, so I would have to extract the images from there anyway. From the saved numpy array, we are able to convert it to either images, or a continuous video with a specified frame rate.

## multimonitor.py

The first thing that this script does is it gets a list of all available cameras. I have a dell webcam that outputs two video streams, one regular, and one infrared. Due to some technical reasons, I decided to exclude the infrared from further processing, however, if you choose to keep it, just pass del_infrared=False to the camera_indices function. This has the potential to be very powerful when the lighting conditions are bad/during night-time/multi-day monitoring. Although, it might need some ironing out.

as far as the recording goes, instead of appending an rgb array to an existing/initialised numpy array and having the flexibility of size, I decided to initialise an array that can hold 1000 480 x (640*n_cams) x 3 arrays. This takes up a big chunk of data up front, but it makes up for it with the speed due to the pre-initialised array. Feel free to modify the value of rec_array_size to change this.

## output_extractor.py

after a video output has been created, if you wanted to extract all the frames of that video into individual png files, tell output_extractor.py which directory to put the png files into, and the name of the video file to read in.

## output_writer.py

this script takes a .npy file saved by multimonitor.py file, and extracts each layer of the array as an image. output directory for the images and the .npy file name will have to be specified.