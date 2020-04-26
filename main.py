from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
import youtube_dl
import getpass

config = {
    'EMAIL': '',
    'PASSWORD': ''
}

login_url = 'https://video.dtu.dk/user/login'


def main():
    # Prompt for login details
    config['EMAIL'] = input("Please enter your DTU email (xxx@dtu.dk or s123456@student.dtu.dk): ")
    config['PASSWORD'] = getpass.getpass("Please enter your DTU password: ")

    # Prompt for video URL
    video_url = input("Please enter the video URL: ")
    print("Hold tight, magic is happening!")

    driver = webdriver.Chrome('./chromedriver')
    driver.get(login_url)
    assert 'Login - DTU - MediaSpace' in driver.title
    elem = driver.find_element_by_name('Login[username]')
    elem.clear()
    elem.send_keys(config['EMAIL'])
    elem = driver.find_element_by_name('Login[password]')
    elem.clear()
    elem.send_keys(config['PASSWORD'])
    elem.send_keys(Keys.RETURN)

    i = True
    while i:
        try:
            expected_url = driver.current_url
            actual_url = "https://video.dtu.dk/"
            assert expected_url == actual_url
            i = False
        except AssertionError:
            time.sleep(1)
            continue

    # Load video page
    driver.get(video_url)
    driver.switch_to.frame(driver.find_element_by_css_selector('#kplayer_ifp'))
    # Get the script
    script = driver.find_element_by_css_selector('body script:nth-child(2)').get_attribute("innerHTML")
    data = (script.splitlines()[2])[37:-1]
    # Load the data into json format
    js = json.loads(data)
    dl_link = js["entryResult"]["meta"]["downloadUrl"]
    title = js["entryResult"]["meta"]["name"]
    # Download video
    ydl_opts = {"outtmpl": title + ".mp4"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([dl_link])


main()