/*
 * To compile: 
 * g++ main.cpp -o  main -I/usr/local/include/ -lraspicam -lraspicam_cv -lopencv_core -lopencv_highgui
 *
 * */
#include <ctime>
#include <iostream>
#include <raspicam/raspicam_cv.h>
using namespace std;

float calculateNDVI(float nir, float g, float b){
	float ndvi = 0.0;
	float top = nir - b;
	float bottom = nir + b;
	//exixte not divide by zero
	if(bottom == 0) bottom = 0.01;
	ndvi = top / bottom;
	return ndvi;
}

void displayImage(cv::Mat image){
	cv::imshow("Imagem original", image);
}
 
int main () {
   
    time_t timerBegin, timerEnd;
    raspicam::RaspiCam_Cv Camera;
    cv::Mat frame;
    float ndviAccumulated, ndviMedium;
    
    //set camera params
    Camera.set( CV_CAP_PROP_FORMAT, CV_8UC1 );
    
    //Open camera
    if (!Camera.open()) {
		cerr << "Error opening the camera" << endl;
		return -1;
	}
    
	while(true) {
		//start time
		time(&timerBegin);
		
		//initialize variables
		ndviAccumulated = 0.0;
		ndviMedium = 0.0;
		
		//frame capture
        Camera.grab();
        Camera.retrieve (frame);
        
        //frame properties
        int width = frame.size().width;
		int height = frame.size().height;
        
        //calculate NDVI
        
        
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
		cout << "\tNumber of pixels: " << (width*height) << endl;
		cout << "\tAccumulated NDVI: " << ndviAccumulated << endl;
		cout << "\tMedium NDVI: " << ndviMedium << endl;
		cout << "########################################" << endl;
		cout << "\tTempo por frame: " << totalTime  << " s" << endl;
		cout << "\tFPS: " << (1 / totalTime) << endl;
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
