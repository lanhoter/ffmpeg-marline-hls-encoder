import os
from os import path
import glob
import subprocess
import urllib
import json
import re
import fnmatch

IN_DIRECTORY = os.getcwd()  # get current input Directory
OUT_DIRECTORY = os.getcwd()+ '/out'  # output directory

#check if the output directory exists, create directory if it is not exist
if os.path.isdir(OUT_DIRECTORY):
        print ('dir exists')
        pass
else:
        print('dir not exists')
        os.mkdir(OUT_DIRECTORY)  
        print('mkdir ok')

#key API
keyApiUrl = 'keyApiUrl'
KeyApiPath = 'KeyApiPath'
# ffmepg

def Process():    
    for filename in glob.glob1(IN_DIRECTORY, '*.*'):
        #only go through files with certain extensions
        if filename.endswith('.mp4'):
            #get filename without extension
            file_name_without_extension = os.path.splitext(filename)[0]
            output_dir = OUT_DIRECTORY + '/' + file_name_without_extension
            #set URL
            keyUrl = keyApiUrl + KeyApiPath + '/' + file_name_without_extension
            content= urllib.urlopen(keyUrl)
            ddict = json.loads(content.read())
            
            if ddict.has_key('message'):
                print ("--------------------------ERROR------------------------------")
                print ("Sorry, cannot return the content key, file name: " + filename)
            else:
                #check if the output folder exists in the system, if No, create folder with filename
                if os.path.isdir(output_dir): 
                    print ("--------------------------ERROR------------------------------")
                    print ('directory exists, file name: ' + filename)
                    pass
                else: os.mkdir(output_dir)
                #fragment videos.
                subprocess.call(
                ["ffmpeg", 
                "-y",
                "-i", filename,
                "-profile:v", "baseline", "-level","3.0",
                "-start_number","0",
                "-hls_time", "10", "-hls_list_size", "0",
                "-f", "hls", 
                file_name_without_extension +"_.m3u8", 
                ])

                for tsfilename in glob.glob1(IN_DIRECTORY, '*.*'):
                #check if the output folder exists in the system, if No, create folder with filename
                    tsfile_name_without_extension = os.path.splitext(tsfilename)[0]
                #only go through files with certain extensions
                    if tsfilename.endswith('.ts'):
                        subprocess.call(
                        ["openssl",
                        "aes-128-cbc",
                        "-e", 
                        "-in",  tsfilename,
                        "-out", tsfile_name_without_extension + "_enc.ts",
                        "-nosalt",
                        "-iv", "0", 
                        "-K", ddict['contentKey']
                        ])
                        subprocess.call("rm %s" % (IN_DIRECTORY + "/" + tsfile_name_without_extension + ".ts"), shell=True)
                        subprocess.call("mv %s %s" % (tsfile_name_without_extension + "_enc.ts", output_dir), shell=True)

                fopen=open(file_name_without_extension + "_.m3u8",'r')

                w_str = ""
                for line in fopen:
                    if re.search('#EXT-X-VERSION:3',line):
                        line=re.sub('#EXT-X-VERSION:3','#EXT-X-VERSION:3\n#EXT-X-KEY:METHOD=AES-128,URI="urn:marlin-drm"' 
                            + "," + 'CID="'+ ddict['contentId'] + '"' ,line)
                        w_str+=line
                    else:   w_str+=line
                wopen=open(file_name_without_extension + "_.m3u8",'w')
                wopen.write(w_str)
                fopen.close()
                wopen.close()

                #add enc           
                wordReplace = open(file_name_without_extension + "_.m3u8", 'r+')
                s=wordReplace.read()
                wordReplace.seek(0,0)
                wordReplace.write(s.replace(".ts","_enc.ts"))
                
               # move all files
                subprocess.call("mv %s %s" % (file_name_without_extension + "_.m3u8", output_dir), shell=True)

def renameM3U8Files(OUT_DIRECTORY):   
    #list filenames in the current directory 
    files=os.listdir(OUT_DIRECTORY)

    #switch file directory
    os.chdir(OUT_DIRECTORY) 

    #scan all filenames in the subfolder
    for fileName in files:
        if os.path.isdir(fileName): 
            renameM3U8Files(fileName)
            os.chdir(os.pardir) 

    #change all the m3u8 file names to master.m3u8
    for i in range(0,len(files)):
        fileNameArray=os.path.splitext(files[i])
        if len(fileNameArray)==2 and (fileNameArray[1]==".m3u8"):
            newFileName="master.m3u8"
            os.rename(files[i],newFileName)
            print ("Rename m3u8 files succeeded: " + files[i])

if __name__ == '__main__':
    Process()
    renameM3U8Files('.')
