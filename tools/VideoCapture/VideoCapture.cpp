#include <opencv/cv.h>
#include <opencv/highgui.h>
#include <iostream>
#include <sys/stat.h>
#include<string.h>
#include<sys/types.h>
#include<dirent.h>


int main(int argc, char **argv)
{
    
    DIR *dp;
    struct dirent * dirp   ;
    char *foldPath = argv[2];
    std::vector<std::string> filenames;

    if((dp = opendir(foldPath)) == NULL){
        std::cout<<"opendir error"<<std::endl;
        exit(1);
    }
    while((dirp = readdir(dp)) != NULL){

        char filename[128];
        // char mp4File[128];
        // strcat(foldPath,new char('/'));
        char videoFile[256];
        sprintf(videoFile,"%s%s", foldPath, dirp->d_name);
        // strcat(videoFile, foldPath);
        // strcat(videoFile, dirp->d_name);
        CvCapture *capture = cvCreateFileCapture(videoFile); //open video
          std::cout<<videoFile<<std::endl;
        int count = 0;
        int period =   (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FPS);
        period = period * atoi(argv[1]);// set the period to the frame capture
        int num = (int)cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_COUNT);
        std::cout<<"period: "<<period<<std::endl<<"num: "<<num<<std::endl;

        if (capture == NULL)
        {
            continue;
        }
        IplImage *frame;
        std::string d_name(dirp->d_name);
        int pos = d_name.find_last_of('.');
        char foldName[256];
        sprintf(foldName, "%s%s", foldPath, (d_name.substr(0,pos)).c_str());
        // strcat(foldName, foldPath);
        // strcat(foldName, );
        // std::cout<<mkdir(foldName,0755)<<std::endl;
        if(mkdir(foldName,0755) == 0){
            bool stop = false;
            std::cout<<"dddddddddddddddd";
            while (1&&!stop)
            {
                for (int i = 0; i < period; i++)
                {
                    frame = cvQueryFrame(capture);
                    if (!frame)
                    {
                        printf("finish!\n");
                        system("pause");
                        stop = true;
                        break;
                    }
                }
                if(stop)
                    continue;
                sprintf(filename, "%s/img_%d.jpg", foldName,count++);
                std::cout<<filename<<std::endl;
                cvSaveImage(filename, frame);
            }
        }else{
            std::cout<<foldName<<std::endl;
        }
        cvReleaseCapture(&capture);
    }
    return 0;
}