import time
import json
from sys import platform, argv
from DTU_VD_functions import *


login_url = 'https://video.dtu.dk/user/login'

def main():
    # Prompt for login details
    config = prompt_config()
    if config['EMAIL'] == '' or config['PASSWORD'] == '': 
        return
    
    #Log in on the webpage.
    driver = open_driver(config, login_url)
    
    args = argv[1:]
    if len(args) == 0:
        #Prompt for video url or category url
        url = input("Please enter the video or category URL: ")
        
        if 'video.dtu.dk/category/' in url:
            urls = read_category(driver,url)
    elif len(args) == 1:
            urls = eval(args[0])
            pathout = None
    elif len(args) == 2:
            urls = eval(args[0])
            pathout = eval(args[1])
        
    download_videos(driver, urls, pathout)
    
if __name__ == '__main__':
    main()
