/*
 * Author: Maik Basso
 * Email: maik@maikbasso.com.br
 * 
 * To compile: 
 * g++ main.cpp -o  main -I/usr/local/include/ -lraspicam -lraspicam_cv -lopencv_core -lopencv_highgui
 *
 * */
#include <ctime>
#include <iostream>
#include <raspicam/raspicam_cv.h>

#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <iostream>
#include <string>
#include <cv.h>
#include <highgui.h>

using namespace std;

void displayImage(cv::Mat image){
	cv::imshow("Imagem original", image);
}
 
int main () {
   
    time_t timerBegin, timerEnd;
    raspicam::RaspiCam_Cv Camera;
    cv::Mat frame, ndvi, top, bottom;
    float cumulativeNdvi, averageNdvi;
    
    //set camera params
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC3);
    
    //Open camera
    if (!Camera.open()) {
		cerr << "Error opening the camera" << endl;
		return -1;
	}
    
	while(true) {
		//start time
		time(&timerBegin);

		//frame capture
        Camera.grab();
        Camera.retrieve (frame);
        
        //frame properties
        int width = frame.size().width;
		int height = frame.size().height;
		
		//initialize variables
		cumulativeNdvi = 0.0;
		averageNdvi = 0.0;
		top = cv::Mat::ones(height, width, CV_32FC1);
		bottom = cv::Mat::ones(height, width, CV_32FC1);
		ndvi = cv::Mat::ones(height, width, CV_32FC1);

        
        //get the image bands
		std::vector<cv::Mat> channels;
        split(frame, channels);
        //b = channels[0];
        //g = channels[1];
        //nir = channels[2];

        //calculate NDVI
        subtract(channels[2], channels[0], top);
		add(channels[2], channels[0], bottom);
		divide(top, bottom, ndvi);
		//http://docs.opencv.org/2.4/modules/core/doc/operations_on_arrays.html
		meanStdDev(ndvi, averageNdvi);
		//averageNdvi = cumulativeNdvi / (width*height);

        //stop time
        time (&timerEnd);
        
        //total time
        double totalTime = difftime(timerEnd, timerBegin);
        
        //statistics
        system("clear");
		cout << "########################################" << endl;
		cout << "######## NDVI C++ by Maik Basso ########" << endl;
		cout << "########################################" << endl << endl;
		cout << "\tFrame size: " << width << "x" << height << endl; 
		cout << "\tPixels per frame: " << (width*height) << endl;
		cout << "\tCumulative NDVI: " << cumulativeNdvi << endl;
		cout << "\taAverage NDVI: " << averageNdvi << endl;
		cout << "########################################" << endl;
		cout << "\tTime per frame: " << totalTime  << " s" << endl;
		cout << "\tFPS: " << ((float) 1 / totalTime) << endl;
		cout << "########################################" << endl;
		
		//display image
		displayImage(frame);
    }
    
    //stop the camera
    Camera.release();
    
    //save image 
    //cv::imwrite("raspicam_cv_image.jpg",image);
    
    return 0;
}