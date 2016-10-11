# -*- coding: utf-8 -*-
"""
Author: Maik Basso
Email: maik@maikbasso.com.br
"""
import time
import numpy as np
import os
import cv2
import picamera
import picamera.array

def calculateNdvi(nir, g, b):
	"""
	Performs the calculation of the NDVI of an image
	"""
	top = (nir.astype(float) - b.astype(float))
	bottom = (nir.astype(float) + b.astype(float))
	# avoid division by zero in the entire array
	bottom[bottom == 0] = 0.01
	ndvi = top / bottom
	return ndvi

def displayImage(img, r, g, b, ndvi):
	"""
	Displays the results
	"""	
	#contrast adjustment
	in_min = np.percentile(ndvi, 5)
	in_max = np.percentile(ndvi, 95)
	out_min = 0.0
	out_max = 255.0
	out = ndvi - in_min
	out *= ((out_min - out_max) / (in_min - in_max))
	out += in_min
	ndviGray = out
	#converts images to acceptable format opencv
	ndviGray = ndviGray.astype(np.uint8)
	#identifying the images
	cv2.putText(r, 'Infrared', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)
	cv2.putText(g, 'Green', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)
	cv2.putText(b, 'Blue', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)
	cv2.putText(ndviGray, 'NDVI-Blue', (0, 20), cv2.FONT_HERSHEY_SIMPLEX, .8, 255)
	#Combines the images into one to display
	height, width = r.shape
	image = np.zeros((2 * height, 2 * width, 3), dtype=np.uint8)
	image[0:height, 0:width, :] = cv2.cvtColor(r, cv2.COLOR_GRAY2RGB)
	image[height:, 0:width, :] = cv2.cvtColor(g, cv2.COLOR_GRAY2RGB)
	image[0:height, width:, :] = cv2.cvtColor(b, cv2.COLOR_GRAY2RGB)
	image[height:, width:, :] = cv2.cvtColor(ndviGray, cv2.COLOR_GRAY2RGB)
	# Display
	cv2.imshow('Original Image', img)
	cv2.imshow('NDVI', image)
	#cv2.imshow('NDVI Color', colorNDVI2(ndvi))

#def colorNDVI2(ndvi):
	#"""
	#This function generates a classified image of NDVI, however it's not finished
	#"""
	#ndvi = np.array([ndvi, ndvi, ndvi])
	#ndvi[ndvi >= 0.941] = 0, 102, 0
	#ndvi[ndvi >= 0.824] = 0, 136, 0
	#ndvi[ndvi >= 0.706] = 0, 187, 0
	#ndvi[ndvi >= 0.588] = 0, 255, 0
	#ndvi[ndvi >= 0.471] = 204, 255, 0
	#ndvi[ndvi >= 0.353] = 255, 255, 0
	#ndvi[ndvi >= 0.235] = 255, 204, 0
	#ndvi[ndvi >= 0.118] = 255, 136, 0
	#ndvi[ndvi >= 0.000] = 255, 0, 0
	#ndvi[ndvi >= -0.118] = 238, 0, 0
	#ndvi[ndvi >= -0.235] = 221, 0, 0
	#ndvi[ndvi >= -0.353] = 204, 0, 0
	#ndvi[ndvi >= -0.471] = 187, 0, 0
	#ndvi[ndvi >= -0.588] = 170, 0, 0
	#ndvi[ndvi >= -0.706] = 153, 0, 0
	#ndvi[ndvi >= -0.824] = 136, 0, 0
	#ndvi[ndvi >= -0.941] = 119, 0, 0
	#ndvi[ndvi < -0.941] = 0, 0, 0
	#return ndvi

def run():
    with picamera.PiCamera() as camera:
        #camera settings
        resolution = [[1920,1080],[1336,768],[1280,720],[1024,768],
        [800,600], [640,480],[320,240], [160,120],[100,133]]
        camera.resolution = reversed(resolution[8])
        camera.framerate = 25
        
        #time to wait for the settings to be applied successfully
        time.sleep(2)

        with picamera.array.PiRGBArray(camera) as stream:
            while True:
				
				startTime = time.time()
				
				#It's important to configure the bands as "bgr" for use in opencv
				camera.capture(stream, format='bgr', use_video_port=True)
				#get the array of the image
				img = stream.array

				#get color bands
				b, g, r = cv2.split(img)

				#calculate the NDVI
				ndvi = calculateNdvi(r, g, b)

				#calculates the average of ndvi region
				cumulativeNdvi = np.sum(ndvi)
				totalOfIndexes = len(ndvi[0]) * len(ndvi)
				averageNdvi = cumulativeNdvi / totalOfIndexes
				
				totalTime = time.time() - startTime
				
				os.system("clear")
				print "#" * 41
				print "#" * 7, "NDVI Python by Maik Basso", "#" * 7
				print "#" * 41
				print "\n"
				print "\tFrame size: %d x %d" %(img.shape[0],img.shape[1])
				print "\tPixels per frame: %d" %(totalOfIndexes)
				print "\tCumulative NDVI: %d" %(cumulativeNdvi)
				print "\tAverage NDVI: %f" %(averageNdvi)
				print "\n"
				print "#" * 41
				print "\tTime per frame: %f s" %(totalTime)
				print "\tFPS: %f" %(1 / totalTime)
				print "#" * 41

				#show images
				displayImage(img, r, g, b, ndvi)
				
				#Delete the contents of a stream.
				stream.truncate(0)

				# If we press ESC then break out of the loop
				key = cv2.waitKey(7) % 0x100
				if key == 27:
					break

    #Clears the cash at the end of the application
    cv2.destroyAllWindows()

#starts the application here
if __name__ == 'main':
	os.system("clear")
	run()
