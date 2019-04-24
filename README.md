# ffmpeg-split

This tool can convert MP4 video into TS fragments and DRM Encrypted.  
  
If there is no MP4 video in the current folder. Nothing will happen.  
  
A Guideline to perform the convert:  
  
    Place the python script under the target folder  
    Open the terminal and type: "Python ffmpegDRMEncoder.py"  
    It will create an output folder named "out" in the current directory.  
    All the encrypted TS files and master.m3u8 playlist will be moved accordingly into the "out" folder.  

Tools may used:  
  
Incase some videos are playing laggy after convert. Please use Handbrake to optimize the orginal video before converting, just use the default setting to optimize the MP4 video.  
   
Link is provided below:
  
Handbrake: https://handbrake.fr/
