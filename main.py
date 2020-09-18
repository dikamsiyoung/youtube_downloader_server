# Import dependencies
from selenium import webdriver
import time, pytube, os

# Setup selenium webdriver
PATH = f"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

# Get channel link from user
channel_link = "https://www.youtube.com/channel/UCtx8VrbY0M7oLgzl5M_ELsg"
videos_link = f'{channel_link}/videos'

# Open videos page
driver.get(videos_link)

# Get channel name
channel_name = driver.find_element_by_class_name("style-scope ytd-channel-name").text
channel_path = f'C:/Users/Mejabi Oluwadurotimi/Downloads/Youtube_Videos/{channel_name}'

# Create new folder
if not os.path.exists(channel_path):
    os.makedirs(channel_path)

# Scroll to the bottom of the page
last_height, new_height = 0, 1

while last_height != new_height:
    last_height = new_height
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.documentElement.scrollHeight;")

# Get all links
links = driver.find_elements_by_id("thumbnail")

# Download all videos
for i, link in enumerate(links):
    youtube = pytube.YouTube(link.get_attribute('href'))
    video = youtube.streams.get_by_itag(135)
    video.download(channel_path)
    print(f'Video {i+1}/{len(links)} downloaded')
    # streams = youtube.streams.all()
    # for i in streams:
    #     print(i)
    # Streams
    # 133 = 240p
    # 134 = 360p
    # 22 = 720p




driver.quit()
