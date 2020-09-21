# Import dependencies
from selenium import webdriver
from IPython import get_ipython
import time
import pytube
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Setup chrome webdriver
PATH = f"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


def open_chrome(channel_link):
    # Get channel link from user
    videos_link = f'{channel_link}/videos'

    # Open videos page
    driver.get(videos_link)


def get_channel_name():
    # Get channel name
    return driver.find_element_by_class_name("style-scope ytd-channel-name").text


def get_profile_pic():
    return driver.find_element_by_id("img").get_attribute("src")


def scroll_to_the_bottom():
    # Scroll to the bottom of the page
    last_height, new_height = 0, 1

    while last_height != new_height:
        last_height = new_height
        driver.execute_script(
            "window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script(
            "return document.documentElement.scrollHeight;")


def get_all_links():
    # Get all links
    return driver.find_elements_by_id("video-title")


def seconds_converter(string_time):
    time_lst = string_time.split(':')
    hour = int(time_lst[0])
    minute = int(time_lst[1])
    second = int(time_lst[2])
    return hour*3600 + minute*60 + second


def create_directory(channel_name):
    channel_path = f'C:/Users/Mejabi Oluwadurotimi/Downloads/Youtube_Videos/{channel_name}'

    # Create new folder
    if not os.path.exists(channel_path):
        os.makedirs(channel_path)

    return channel_path


def download_all_videos(channel_name, video_links):
    channel_path = create_directory(channel_name)

    # Download all videos
    for i, link in enumerate(video_links):
        youtube = pytube.YouTube(link)
        video = youtube.streams.get_by_itag(135)
        video.download(channel_path)
        print(f'Video {i+1}/{len(video_links)} downloaded')
        # streams = youtube.streams.all()
        # for i in streams:
        #     print(i)
        # Streams
        # 133 = 240p
        # 134 = 360p
        # 22 = 720p


@app.route("/get_channel_details", methods=['GET', 'POST'])
def get_channel_details():
    if request.method == "GET":
        return jsonify({"response": "Channel Details endpoint"})
    elif request.method == "POST":
        req_json = request.json
        channel_link = req_json["channel_link"]
        open_chrome(channel_link)
        channel_name = get_channel_name()
        profile_pic = get_profile_pic()
        scroll_to_the_bottom()
        links = get_all_links()
        video_links = []
        for link in links:
            video_links.append(link.get_attribute("href"))
        return jsonify({"channel_details": {
            "channel_name": channel_name,
            "profile_pic": profile_pic,
            "num_of_videos": len(links),
            "video_links": video_links
        }})


@app.route("/download_videos", methods=['GET', 'POST'])
def download_videos():
    if request.method == "GET":
        return jsonify({"response": "Channel Details endpoint"})
    elif request.method == "POST":
        req_json = request.json
        video_links = req_json["video_links"]
        channel_name = req_json["channel_name"]
        download_all_videos(channel_name, video_links)
        return jsonify({"res":"done"})


@app.route("/download_snippet", methods=['GET', 'POST'])
def download_snippet(video_link, start, duration, filename):
    if request.method == "GET":
        return jsonify({"response": "Channel Details endpoint"})
    elif request.method == "POST":
        get_ipython().getoutput('pip install youtube-dl')
        get_ipython().getoutput('pip install ffmpeg')
        start = seconds_converter(start)
        duration = seconds_converter(duration)
        url = get_ipython().getoutput('youtube-dl -f 22 -g "{video_link}"')
        result = get_ipython().getoutput(f'ffmpeg -ss {start} -i "{url[0]}" -t {duration} -c copy "{filename}"')
        return jsonify({"res": "done"})


# driver.quit()
if __name__ == "__main__":
    app.run(debug=True)
