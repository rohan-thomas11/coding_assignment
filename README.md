# coding_assignment

1. After getting some error at first, I found that there was an invalid image in the dataset. Also, there was a really low-resolution image.
2. I have a 'del_img' list, which stores the names of the images that are to be deleted. I loop through all the images. I then set different 'black_mask' for the different cameras, to cut out unnecessary portions of the image. Then I check the resolution of the image, and if it too low, append the name of the image to the 'del_img' list. I also check if the image is invalid, and if yes, also append it to the list. Then I resize the image to 480x480 pixels, and pass it through the 'preprocess_image_change_detection()'. Then I loop again through the rest of the images from the same camera (from camera-ID), and check if the images hava a score of less than 3000. If score is less than 3000, I'll remove the second image, else I'll keep it.
3. I chose the Gaussian blur radii to be 9, 11, 15 and 17, and a minimum contour area of 100, just through trial and error.
4. To remove similar images that are only "different" due to the time of the day in which the image was captured (night, day).
